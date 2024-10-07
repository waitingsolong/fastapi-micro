from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
