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
        result = f'Ciao sono up and running ed ho ricevuto --> "{message}"'
        result = {'text': result, 'status_code': True}
        print("Messaggio ricevuto: ", message)

        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MicroServiceServicer_to_server(MicroServiceService(), server)
    server.add_insecure_port('[::]:51314')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()