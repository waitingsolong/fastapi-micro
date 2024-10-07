import threading
from app.utils.handlers import setup_exception_handlers
from app.microservices.auth.core.mw import AuthMiddleware
from fastapi import FastAPI
from app.microservices.auth.api.v1 import auth, healthcheck
from app.microservices.auth.grpc.server import serve as grpc_serve

app = FastAPI()

setup_exception_handlers(app)

excluded_paths = ["/auth/login", "/auth/register", "/auth/validate"]
app.add_middleware(AuthMiddleware, excluded_paths=excluded_paths)

app.include_router(auth.router)
app.include_router(healthcheck.router)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_grpc():
    grpc_serve()

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    grpc_thread = threading.Thread(target=start_grpc)

    fastapi_thread.start()
    grpc_thread.start()

    fastapi_thread.join()
    grpc_thread.join()
