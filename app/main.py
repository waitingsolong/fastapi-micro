import grpc
from fastapi import FastAPI
from app.microservices.news_microservice import news_pb2, news_pb2_grpc
from app.microservices.users_microservice import users_pb2, users_pb2_grpc


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World from FastAPI!"}


@app.get("/news/")
async def get_news():
    with grpc.insecure_channel('news:50051') as channel:
        stub = news_pb2_grpc.NewsServiceStub(channel)
        response = stub.GetNews(news_pb2.NewsRequest())
    return {"message": response.message}


@app.get("/users/")
async def get_users():
    with grpc.insecure_channel('users:50052') as channel:
        stub = users_pb2_grpc.UsersServiceStub(channel)
        response = stub.GetUsers(users_pb2.UserRequest())
    return {"message": response.message}
