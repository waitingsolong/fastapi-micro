from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.microservices.auth.core.config import settings
from app.microservices.auth.core.security import verify_token
from app.microservices.auth.schemas.auth import FakeToken

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_token_data(request: Request):
    if settings.DISABLE_AUTH:
        return FakeToken().model_dump()
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = auth_header.split(" ")[1] if " " in auth_header else None
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    try:
        token_data = verify_token(token)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    
    return token_data