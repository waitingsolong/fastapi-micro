import re
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

async def can_connect_to_database(engine):
    """
    Check if a database connection can be established.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print(f"Successfully connected to database: {engine.url}")
        return True
    except Exception as e:
        print(f"Error connecting to database {engine.url}:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        if hasattr(e, '__cause__'):
            print(f"Cause: {e.__cause__}")
        return False

async def create_database_if_not_exists(postgres_uri):
    """
    Create the database if it does not exist.
    """
    # Extract the database name from the URL
    match = re.search(r'/([^/]+)$', postgres_uri)
    if not match:
        raise ValueError("Could not extract database name from POSTGRES_URI.")
    
    database_name = match.group(1)  # Get the database name (e.g., 'auth')

    # Create a new URI for connecting to the default postgres database
    default_uri = re.sub(r'@[^/]+/', '@localhost/', postgres_uri).replace(database_name, "postgres")

    # Create an engine for connecting to the default database
    default_engine = create_async_engine(default_uri, future=True, echo=True, isolation_level="AUTOCOMMIT")

    # Check if the database exists and create it if it doesn't
    try:
        async with default_engine.connect() as conn:
            result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"))
            exists = result.scalar() is not None

            if not exists:
                # Database does not exist, create it
                await conn.execute(text(f"CREATE DATABASE {database_name}"))
                print(f"Database '{database_name}' created successfully.")
            else:
                print(f"Database '{database_name}' already exists.")

    except OperationalError as e:
        print(f"Error checking or creating database '{database_name}': {str(e)}")

    # Verify the database creation
    try:
        async with default_engine.connect() as conn:
            result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"))
            exists = result.scalar() is not None

            if exists:
                print(f"Database '{database_name}' successfully verified.")
            else:
                print(f"Error: Database '{database_name}' was not created.")

    except OperationalError as e:
        print(f"Error verifying database '{database_name}': {str(e)}")

    # Test connection to the newly created database
    new_engine = create_async_engine(postgres_uri, future=True, echo=True)
    if await can_connect_to_database(new_engine):
        print(f"Successfully connected to the new database '{database_name}'.")
    else:
        print(f"Failed to connect to the new database '{database_name}'.")