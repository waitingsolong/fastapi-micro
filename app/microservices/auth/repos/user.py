from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import select for async querying
from app.microservices.auth.models.user import User
from app.microservices.auth.schemas.auth import UserCreate
from app.microservices.auth.core.security import get_password_hash

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role="football_fan",
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
