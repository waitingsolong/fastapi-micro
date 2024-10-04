import asyncio
from fastapi import FastAPI
from app.microservices.auth.api.v1 import auth, healthcheck
from app.microservices.auth.grpc.server import serve as grpc_serve

app = FastAPI()

app.include_router(auth.router, prefix="/v1")  
app.include_router(healthcheck.router, prefix="/v1")

async def start_fastapi():
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def start_grpc():
    grpc_serve() 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            start_fastapi(),
            start_grpc()
        )
    )
