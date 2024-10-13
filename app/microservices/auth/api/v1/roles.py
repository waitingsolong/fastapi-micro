from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.microservices.auth.core.deps import get_token_data
from app.microservices.auth.core.permissions import require_role
from app.microservices.auth.models.user import User
from app.microservices.auth.schemas.auth import RoleAssignRequest
from app.microservices.auth.services.user import get_user_by_username
from app.microservices.auth.utils.db import get_db

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)

@router.put("/assign")
async def assign_role(role_request: RoleAssignRequest, token: dict = Depends(require_role("admin")), db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, username=role_request.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.role = role_request.role 
    await db.commit()
    return {"message": f"Role '{role_request.role}' assigned to user '{role_request.username}'"}

@router.get("/amiadmin")
async def admin_endpoint(token: dict = Depends(require_role("admin"))):
    return {"message": "Welcome, admin!"}

@router.get("/mine")
async def get_my_role(request: Request):
    token = await get_token_data(request)
    return {"role": token.get("role")}

@router.get("/role/by_username/{username}", response_model=dict)
async def get_role_by_username(username: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"role": user.role.value}

@router.get("/role/by_id/{user_id}", response_model=dict)
async def get_role_by_userid(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"role": user.role.value}
