import grpc
from concurrent import futures
import time
import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2
from threading import Thread

#
# class MicroServiceService(pb2_grpc.MicroServiceServicer):
#
#     def __init__(self, *args, **kwargs):
#         pass
#
#     def GetMicroServiceResponse(self, request, context):
#
#         # get the string from the incoming request
#         message = request.message
#         result = f'Ciao sono up and running ed ho ricevuto --> "{message}"'
#         result = {'body': result, 'received': True}
#         print("Messaggio ricevuto: ", message)
#
#         return pb2.MessageResponse(**result)
#


class gRPCThread(Thread, pb2_grpc.MicroServiceServicer):
    # micro_service_service = MicroServiceService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def __init__(self):
        Thread.__init__(self)

    # def run(self):
    #     print("Thread http started")
    #     global flask_host, flask_port
    #
    #     logging.basicConfig(level=logging.INFO)
    #
    #     self.app.run(host=flask_host, port=flask_port)
    #     print("Thread '" + self.name + "closed")

    def GetMicroServiceResponse(self, request, context):
        try:
            HttpThread.app.logger.info('Request Received')
            mss_test_ingress.labels("s0").inc(1)  # Increment by 1
            mss_test_summary.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(100)
            # mss_test_ingress.inc(1)  # Increment by 1
            # Execute the internal service
            print("*************** INTERNAL SERVICE STARTED ***************")
            start_local_processing = time.time()
            body = run_internal_service(my_work_model["internal_service"])
            local_processing_latency = time.time() - start_local_processing
            LOCAL_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path).observe(local_processing_latency)
            RESPONSE_SIZE.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(len(body))
            print("len(body): %d" % len(body))
            print("############### INTERNAL SERVICE FINISHED! ###############")

            # Execute the external services
            print("*************** EXTERNAL SERVICES STARTED ***************")
            if len(my_service_mesh) > 0:
                service_error_dict = run_external_service(my_service_mesh, work_model)
                pprint(service_error_dict)
                if len(service_error_dict):
                    HttpThread.app.logger.error("Error in request external services")
                    HttpThread.app.logger.error(service_error_dict)
                    return make_response(json.dumps({"message": "Error in same external services request"}), 500)
            print("############### EXTERNAL SERVICES FINISHED! ###############")

            response = make_response(body)
            response.mimetype = "text/plain"
            return response
            # return json.dumps(body), 200
            # return json.dumps(service_mesh[ID]), 200
        except Exception as err:
            print(traceback.format_exc())
            return json.dumps({"message": "Error"}), 500

        # get the string from the incoming request
        message = request.message
        result = f'Ciao sono up and running ed ho ricevuto --> "{message}"'
        result = {'body': result, 'received': True}
        print("Messaggio ricevuto: ", message)

        return pb2.MessageResponse(**result)

    def run(self):
        pb2_grpc.add_MicroServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port('[::]:51313')
        self.server.start()
        self.server.wait_for_termination()


if __name__ == '__main__':
    grpc_prova = gRPCThread()
    grpc_prova.run()
