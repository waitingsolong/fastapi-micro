import grpc
from concurrent import futures
from app.microservices.users_microservice import users_pb2
from app.microservices.users_microservice import users_pb2_grpc


class UsersService(users_pb2_grpc.UsersServiceServicer):
    def GetUsers(self, request, context):
        return users_pb2.UserResponse(message="Hello from Users via gRPC!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServiceServicer_to_server(UsersService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
