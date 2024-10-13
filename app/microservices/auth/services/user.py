from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from app.microservices.auth.core.roles import DEFAULT_ROLE
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
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    db_user = User(
        id=uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=DEFAULT_ROLE,
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user