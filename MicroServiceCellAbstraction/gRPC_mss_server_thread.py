import grpc
from concurrent import futures
import time
import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2
from threading import Thread
from InternalServiceExecutor import run_internal_service
from ExternalServiceExecutor import run_external_service, init_gRPC, init_REST
from pprint import pprint
import json

import logging

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

# my_service_mesh = [{"seq_len": 2, "services": ["s1", "s3"]}, {"seq_len": 2, "services": ["s2"]}]
my_service_mesh = [{"seq_len": 2, "services": ["s1"]}]

work_model_test = {
   "s0":{
      "internal_service":{
         "colosseum":{

         }
      },
      "url":"s0.default.svc.cluster.local",
      "path":"/api/v1",
      "image":"lucapetrucci/microservice:latest",
      "namespace":"default"
   },
   "s1":{
      "internal_service":{
         "compute_pi":{
            "mean_bandwidth":11,
            "range_complexity":[
               600,
               600
            ]
         }
      },
      # "url":"s1.default.svc.cluster.local",
      "url":"localhost",
      "path":"/api/v1",
      "image":"lucapetrucci/microservice:latest",
      "namespace":"default"
   },
   "s2":{
      "internal_service":{
         "compute_pi":{
            "mean_bandwidth":11,
            "range_complexity":[
               101,
               101
            ]
         }
      },
      "url":"localhost",
      "path":"/api/v1",
      "image":"lucapetrucci/microservice:latest",
      "namespace":"default"
   },
    "s3": {
        "internal_service": {
            "colosseum": {}
        },
        "url": "localhost",
        "path": "/api/v1",
        "image": "lucapetrucci/microservice:latest",
        "namespace": "default"
    }
}
ID = "s0"

my_work_model = work_model_test[ID]


class gRPCThread(Thread, pb2_grpc.MicroServiceServicer):
    # micro_service_service = MicroServiceService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

    def __init__(self):
        Thread.__init__(self)

    def GetMicroServiceResponse(self, request, context):
        try:
            logging.info('Request Received')
            # mss_test_ingress.labels("s0").inc(1)  # Increment by 1
            # mss_test_summary.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(100)
            # mss_test_ingress.inc(1)  # Increment by 1
            # Execute the internal service
            print("*************** INTERNAL SERVICE STARTED ***************")
            start_local_processing = time.time()
            body = run_internal_service(my_work_model["internal_service"])
            local_processing_latency = time.time() - start_local_processing
            # LOCAL_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path).observe(local_processing_latency)
            # RESPONSE_SIZE.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(len(body))
            print("len(body): %d" % len(body))
            print("############### INTERNAL SERVICE FINISHED! ###############")

            # Execute the external services
            print("*************** EXTERNAL SERVICES STARTED ***************")
            if len(my_service_mesh) > 0:
                service_error_dict = run_external_service(my_service_mesh, work_model_test)
                pprint(service_error_dict)
                if len(service_error_dict):
                    logging.error("Error in request external services")
                    logging.error(service_error_dict)
                    # return make_response(json.dumps({"message": "Error in same external services request"}), 500)

                    # return json.dumps({"message": "Error in same external services request"}), 500
                    result = {'text': f"Error in same external services request", 'status_code': False}
                    return pb2.MessageResponse(**result)
            print("############### EXTERNAL SERVICES FINISHED! ###############")

            message = request.message
            print(f'I am service: {ID} and I received this message: --> "{message}"')
            result = {'text': body, 'status_code': True}
            return pb2.MessageResponse(**result)
        except Exception as err:
            print("Error: in GetMicroServiceResponse,", err)
            message = request.message
            print(f'I am service: {ID} and I received this message: --> "{message}"')
            result = {'text': f"Error: in GetMicroServiceResponse, {str(err)}", 'status_code': False}
            return pb2.MessageResponse(**result)


    def run(self):
        pb2_grpc.add_MicroServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port('[::]:51313')
        self.server.start()
        self.server.wait_for_termination()


if __name__ == '__main__':
    grpc_prova = gRPCThread()
    grpc_prova.run()
