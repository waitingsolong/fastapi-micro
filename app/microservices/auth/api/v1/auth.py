from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.microservices.auth.models.user import User
from auth.schemas.auth import Token, UserCreate, UserResponse, LoginRequest, LoginResponse
from auth.repos.user import get_user_by_username, create_user
from auth.core.security import create_access_token, verify_password, verify_token
from auth.core.db import get_db
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user_data = user.model_dump()
    user_data["role"] = "football_fan" 
    
    new_user = create_user(db, UserCreate(**user_data))
    return new_user

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=login_data.username)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": "football_fan"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(verify_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": token["sub"], "role": token["role"]}

@router.post("/assign-role")
def assign_role(username: str, role: str, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    if token is None or token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign roles")
    
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.role = role
    db.commit()
    return {"message": f"Role '{role}' assigned to user '{username}'"}
