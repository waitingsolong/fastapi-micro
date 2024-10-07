import grpc
from concurrent import futures
from app.microservices.auth.grpc import auth_pb2_grpc

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
