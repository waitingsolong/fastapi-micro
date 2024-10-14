import threading
from app.microservices.users.utils.docs_redirect import setup_docs_redirects
from app.utils.handlers import add_cors_middleware, setup_exception_handlers
from fastapi import FastAPI
from app.microservices.users.api.v1 import healthcheck, players, fans

app = FastAPI(docs_url=   '/users/docs',
              redoc_url=  '/users/redoc',
              openapi_url='/users/openapi.json')

# add_cors_middleware
setup_exception_handlers(app)

app.include_router(players.router)
app.include_router(fans.router)
app.include_router(healthcheck.router)

setup_docs_redirects(app)

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=start_fastapi)
    fastapi_thread.start()
    fastapi_thread.join()
