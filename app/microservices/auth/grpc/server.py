import grpc
from concurrent import futures
from . import auth_pb2
from . import auth_pb2_grpc

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def GetAuth(self, request, context):
        return auth_pb2.AuthResponse(message="Hello from Auth via gRPC!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()
