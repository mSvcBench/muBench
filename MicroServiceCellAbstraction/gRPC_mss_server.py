import grpc
from concurrent import futures
import time
import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2


class MicroServiceService(pb2_grpc.MicroServiceServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetMicroServiceResponse(self, request, context):

        # get the string from the incoming request
        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'body': result, 'received': True}

        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MicroServiceServicer_to_server(MicroServiceService(), server)
    server.add_insecure_port('[::]:51313')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()