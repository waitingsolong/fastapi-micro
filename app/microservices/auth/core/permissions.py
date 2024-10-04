from fastapi import HTTPException, Depends
from app.microservices.auth.core.security import verify_token
from app.microservices.auth.core.roles import roles

def require_permission(permission: str):
    def permission_decorator(token: str = Depends(verify_token)):
        user_role = token.get("role")
        if user_role not in roles or permission not in roles[user_role]:
            raise HTTPException(status_code=403, detail="Permission denied")
        return token
    return permission_decorator
