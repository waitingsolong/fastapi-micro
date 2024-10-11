from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.db import get_db   
from app.microservices.auth.core.deps import get_token_data
from app.microservices.auth.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token
)
from app.microservices.auth.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
    TokenData,
    RefreshRequest,
    RoleAssignRequest,
    UserResponse
)
from app.microservices.auth.services.user import get_user_by_username, create_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterRequest, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = await create_user(db, user)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": new_user.username, "role": new_user.role},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": new_user.username, "role": new_user.role},
        expires_delta=refresh_token_expires
    )

    return RegisterResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        role=new_user.role
    )

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_in_db = await get_user_by_username(db, username=user.username)
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_in_db.username, "role": user_in_db.role}, 
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": user_in_db.username, "role": user_in_db.role}, 
        expires_delta=refresh_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_request: RefreshRequest):
    token_data = verify_token(refresh_request.refresh_token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token_expires = timedelta(minutes=30)
    new_access_token = create_access_token(
        data={"sub": token_data["sub"], "role": token_data["role"]}, 
        expires_delta=access_token_expires
    )
    return TokenResponse(
        access_token=new_access_token, 
        token_type="bearer"
    )

@router.post("/assign-role")
async def assign_role(role_request: RoleAssignRequest, token: dict = Depends(get_token_data), db: AsyncSession = Depends(get_db)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign roles")

    db_user = await get_user_by_username(db, username=role_request.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.role = role_request.role
    await db.commit()
    return {"message": f"Role '{role_request.role}' assigned to user '{role_request.username}'"}

@router.get("/me", response_model=UserResponse)
async def check_me(token: dict = Depends(get_token_data), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username=token["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        username=user.username,
        email=user.email,
        role=user.role
    )

@router.post("/validate", response_model=TokenData)
async def validate_auth(token_data: TokenData = Depends(get_token_data)):  
    return token_data  
