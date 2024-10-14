import threading
from app.utils.handlers import add_cors_middleware, setup_exception_handlers
from fastapi import FastAPI
from app.microservices.comments.api.v1 import healthcheck
from app.microservices.comments.api.v1 import comments

app = FastAPI(docs_url=   '/comments/docs',
              redoc_url=  '/comments/redoc',
              openapi_url='/comments/openapi.json')

# add_cors_middleware
setup_exception_handlers(app)

app.include_router(comments.router)
app.include_router(healthcheck.router)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()
    fastapi_thread.join()
