import os
import subprocess
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from app.microservices.auth.core.config import settings as auth_settings
from app.microservices.media.core.config import settings as media_settings
from app.microservices.matches.core.config import settings as matches_settings
from app.microservices.users.core.config import settings as users_settings
from app.utils.db import can_connect_to_database, create_database_if_not_exists

# Usage: 
# > python -m scripts.pg_migrate

# assert: databases must exist

microservices = [
    {"name": "auth", "pg_uri": auth_settings.POSTGRES_URI, "migrations_path": "./migrations/auth"},
    {"name": "media", "pg_uri": media_settings.POSTGRES_URI, "migrations_path": "./migrations/media"},
    {"name": "matches", "pg_uri": matches_settings.POSTGRES_URI, "migrations_path": "./migrations/matches"},
    {"name": "users", "pg_uri": users_settings.POSTGRES_URI, "migrations_path": "./migrations/users"},
]

async def create_databases_if_not_exist(microservices):
    for microservice in microservices:
        await create_database_if_not_exists(microservice["pg_uri"])
    
async def table_exists(connection, table_name):
    """
    Check if a given table exists in the database.
    """
    query = text(f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables 
            WHERE table_name=:table_name
        )
    """)
    result = await connection.execute(query, {"table_name": table_name})
    return result.scalar()

async def run_alembic_revision(microservice, message):
    """
    Generate an Alembic revision for the specified microservice.
    """
    result = subprocess.run(
        ["alembic", "-c", os.path.join(microservice["migrations_path"], "alembic.ini"), "revision", "--autogenerate", "-m", message],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    
    print(result.stdout.decode())  # Command output
    print(result.stderr.decode())  # Errors, if any
    return result.returncode == 0

async def run_alembic_upgrade(microservice, initial=False):
    """
    Run Alembic upgrade for the specified microservice. 
    If `initial` is True, it skips checking for the `alembic_version` table and directly applies migrations.
    """
    print(f"Running migrations for microservice: {microservice['name']}")
    engine = create_async_engine(microservice["pg_uri"], future=True, echo=True)
    
    print(f"Attempting to connect to the database for {microservice['name']}")
    if not await can_connect_to_database(engine):
            print(f"Error: Could not connect to the database for {microservice['name']}")
            return False    

    # Check if alembic_version table exists
    async with engine.connect() as connection:
        if not initial:
            if await table_exists(connection, "alembic_version"):
                print("The 'alembic_version' table exists. Running migrations...")
            else:
                print("The 'alembic_version' table does not exist. Applying initial migration...")
                # Apply the first migration, which will create the `alembic_version` table
                return await apply_initial_migration(microservice)
        else:
            print("Skipping table existence check, directly running initial migration...")
            return await apply_initial_migration(microservice)

    return await apply_migrations(microservice)

async def apply_initial_migration(microservice):
    """
    Applies the initial migration for the microservice (creates alembic_version and runs the migrations).
    """
    # Create the first migration if needed
    if not await run_alembic_revision(microservice, f"Initial migration for {microservice['name']}"):
        print(f"Error: Failed to generate initial migration for {microservice['name']}.")
        return False
    
    # Apply the migration (alembic upgrade head)
    return await apply_migrations(microservice)

async def apply_migrations(microservice):
    """
    Runs the Alembic upgrade command to apply all migrations.
    """
    print("Running migrations...")
    upgrade_result = subprocess.run(
        ["alembic", "-c", os.path.join(microservice["migrations_path"], "alembic.ini"), "upgrade", "head"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    
    # Print output
    print(upgrade_result.stdout.decode())
    print(upgrade_result.stderr.decode())
    
    # Check if the migration was successful
    if upgrade_result.returncode != 0:
        print(f"Error: Migration failed for {microservice['name']}.")
        return False

    print(f"Migration for {microservice['name']} completed successfully.")
    return True

async def main():
    for microservice in microservices:
        await create_database_if_not_exists(microservice["pg_uri"])
        print(f"Waiting for database {microservice['name']} to be ready...")
        await asyncio.sleep(2)  # Ждем 2 секунды после создания каждой базы данных

    # Выполняем миграции последовательно
    for microservice in microservices:
        print(f"\nStarting migration for {microservice['name']}")
        success = False
        retry_count = 1
        
        while not success and retry_count > 0:
            try:
                success = await run_alembic_upgrade(microservice)
                if success:
                    print(f"Migration for {microservice['name']} completed successfully.")
                else:
                    print(f"Migration for {microservice['name']} failed.")
            except Exception as e:
                print(f"Error during migration for {microservice['name']}: {str(e)}")
            
            if not success:
                retry_count -= 1
                if retry_count > 0:
                    print(f"Retrying migration for {microservice['name']} in 5 seconds... ({retry_count} attempts left)")
                    await asyncio.sleep(5)
                else:
                    print(f"All retry attempts for {microservice['name']} have been exhausted.")

    print("\nMigration Summary:")
    for microservice in microservices:
        status = "Success" if await check_migration_status(microservice) else "Failed"
        print(f"{microservice['name']}: {status}")
        
async def check_migration_status(microservice):
    engine = create_async_engine(microservice["pg_uri"], future=True)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            return version is not None
    except Exception as e:
        print(f"Error checking migration status for {microservice['name']}: {str(e)}")
        return False

async def create_and_migrate():
    await create_databases_if_not_exist(microservices)
    
    await asyncio.sleep(2)
    
    await main()
    
if __name__ == "__main__":
    asyncio.run(create_and_migrate())
