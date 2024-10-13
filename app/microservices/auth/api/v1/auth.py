from fastapi import APIRouter, Request, Response, HTTPException, Depends
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.auth.utils.db import get_db   
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
        data={"sub": new_user.username, "role": new_user.role.value},
        expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": new_user.username, "role": new_user.role.value},
        expires_delta=refresh_token_expires
    )

    return RegisterResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        role=new_user.role.value
    )

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
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

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Strict', expires=access_token_expires.total_seconds())
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='Strict', expires=refresh_token_expires.total_seconds())

    return {"message": "Login successful"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    token_data = verify_token(refresh_token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token_expires = timedelta(minutes=30)
    new_access_token = create_access_token(
        data={"sub": token_data["sub"], "role": token_data["role"]}, 
        expires_delta=access_token_expires
    )

    response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True, samesite='Strict', expires=access_token_expires.total_seconds())

    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def check_me(request: Request, db: AsyncSession = Depends(get_db)):
    token = await get_token_data(request)
    user = await get_user_by_username(db, username=token["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        username=user.username,
        email=user.email,
        role=user.role.value
    )

@router.post("/validate-real", response_model=TokenData)
async def real_validate_auth(request: Request):
    return await get_token_data(request, disableAuth=False)

@router.post("/validate", response_model=TokenData)
async def validate_auth(request: Request):
    return await get_token_data(request)
