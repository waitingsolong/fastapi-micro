from pydantic import BaseModel, EmailStr
from app.microservices.auth.core.roles import Role

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RoleAssignRequest(BaseModel):
    username: str
    role: Role 

class TokenData(BaseModel):
    sub: str
    role: Role  

class FakeToken(TokenData):
    def __init__(self, sub: str = "admin", role: Role = Role.admin):
        super().__init__(sub=sub, role=role)

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    role: Role  

class RegisterRequest(UserCreate): 
    pass

class RegisterResponse(UserResponse): 
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
