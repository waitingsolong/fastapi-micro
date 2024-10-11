import threading
from app.utils.handlers import setup_exception_handlers
from fastapi import FastAPI
from app.microservices.news.api.v1 import news, healthcheck

app = FastAPI(docs_url=   '/news/docs',
              redoc_url=  '/news/redoc',
              openapi_url='/news/openapi.json')

setup_exception_handlers(app)

# # TODO
# from app.microservices.auth.core.mw import AuthMiddleware
# excluded_paths = ["/auth/login", "/auth/register", "/auth/validate"]
# app.add_middleware(AuthMiddleware, excluded_paths=excluded_paths)

app.include_router(news.router)
app.include_router(news.wip_router)
app.include_router(healthcheck.router)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()
    fastapi_thread.join()
