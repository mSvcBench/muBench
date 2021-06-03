import grpc
import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2


class MicroServiceClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 51313

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.MicroServiceStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.Message(message=message)
        print(f'{message}')
        return self.stub.GetMicroServiceResponse(message)


if __name__ == '__main__':
    client = MicroServiceClient()
    result = client.get_url(message="Ciao")
    print(f'{result}')