import grpc
from concurrent import futures
import news_pb2
import news_pb2_grpc

class NewsService(news_pb2_grpc.NewsServiceServicer):
    def GetNews(self, request, context):
        return news_pb2.NewsResponse(message="Hello from News via gRPC!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    news_pb2_grpc.add_NewsServiceServicer_to_server(NewsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()