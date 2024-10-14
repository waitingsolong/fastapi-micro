import threading

from app.utils.handlers import add_cors_middleware, setup_exception_handlers
from fastapi import FastAPI
from app.microservices.matches.api.v1 import matches, healthcheck

app = FastAPI(docs_url=   '/matches/docs',
              redoc_url=  '/matches/redoc',
              openapi_url='/matches/openapi.json')

# add_cors_middleware
setup_exception_handlers(app)

app.include_router(matches.router)
app.include_router(healthcheck.router)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()
    fastapi_thread.join()
