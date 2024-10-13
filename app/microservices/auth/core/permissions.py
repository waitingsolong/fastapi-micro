from fastapi import HTTPException, Depends
from app.microservices.auth.core.deps import get_token_data
from app.microservices.auth.core.roles import roles

def require_permission(permission: str):
    def permission_decorator(token: str = Depends(get_token_data)):
        user_role = token.get("role")
        if user_role not in roles or permission not in roles[user_role]:
            raise HTTPException(status_code=403, detail="Permission denied")
        return token
    return permission_decorator

def require_role(required_role: str):
    def role_decorator(token: dict = Depends(get_token_data)):
        user_role = token.get("role")
        if user_role != required_role:
            raise HTTPException(status_code=403, detail="Role required: {}".format(required_role))
        return token
    return role_decorator
