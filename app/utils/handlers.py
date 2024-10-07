from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.microservices.auth.main import app as auth_app

@auth_app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@auth_app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )
    
    
# Usage: 
    
# hardcode for all apps

# in app's main.py:
# from app.utils import handlers
