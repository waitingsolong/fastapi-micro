from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.microservices.auth.core.security import verify_token
from app.microservices.auth.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: list = None):

        super().__init__(app)
        if excluded_paths is None:
            excluded_paths = []
        self.excluded_paths = excluded_paths

    async def dispatch(self, request: Request, call_next):
        if settings.DISABLE_AUTH:
            return await call_next(request)
        
        for path in self.excluded_paths:
            if request.url.path.startswith(path):
                return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})

        token = auth_header.split(" ")[1] if " " in auth_header else None
        if not token:
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        try:
            verify_token(token)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

        return await call_next(request)
