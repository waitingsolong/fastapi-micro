import threading
from app.utils.handlers import setup_exception_handlers
from fastapi import FastAPI
from app.microservices.media.api.v1 import media, healthcheck

app = FastAPI(docs_url=   '/media/docs',
              redoc_url=  '/media/redoc',
              openapi_url='/media/openapi.json')

setup_exception_handlers(app)

app.include_router(media.router)
app.include_router(healthcheck.router)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()
    fastapi_thread.join()
