import random
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import time
import grpc
import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2
from pprint import pprint

work_model = dict()
gRPC_connections = dict()

# REQUEST_METHOD = "REST"
REQUEST_METHOD = "gRPC"


def request_REST(service):
    return requests.get(f'{work_model[service]["url"]}{work_model[service]["path"]}')


def request_gRPC(service):
    print("sono rpc")


def init_gRPC(my_service_mesh, ID, work_model):

    global gRPC_connections
    server_port = 51313
    my_work_model = work_model[ID]

    for group in my_service_mesh:
        print(group)
        for service in group["services"]:
            print(service)
            host = f'{work_model[service]["url"]}'
            print(host)
            # instantiate a channel
            channel = grpc.insecure_channel(
                '{}:{}'.format(host, server_port))
            # bind the client and the server
            gRPC_connections[service] = pb2_grpc.MicroServiceStub(channel)

    message = pb2.Message(message="CIAO")
    print(f'{message}')
    print(gRPC_connections["s2"].GetMicroServiceResponse(message))


def external_service(group, request_function):
    print("**** Start SERVICES nel thread: %s" % str(group))
    seq_len = len(group["services"])
    if group["seq_len"] < len(group["services"]):
        seq_len = group["seq_len"]
    # Randomly select seq_len elements from services in the group
    selected_services = random.sample(group["services"], k=seq_len)
    service_error_dict = dict()
    service_error_flag = False
    for service in selected_services:
        # sleep_time = random.randint(2, 5)
        # print("**** Service: %s -- Sleep for %d" % (service, sleep_time))
        # time.sleep(sleep_time)
        try:
            # "url": "http://s0.default.svc.cluster.local",
            # "path": "/api/v1",
            r = request_function(service)
            print("Service: %s -> Status_code: %s -- len(text): %d" % (service, r.status_code, len(r.text)))

        except Exception as err:
            service_error_dict[service] = err
            service_error_flag = True
            print("Error in request external service %s -- %s" % (service, str(err)))

    print("#### SERVICE Done!")
    return service_error_flag, service_error_dict


def run_external_service_REST(services_group, model):
    print("** EXTERNAL SERVICES")
    global work_model
    service_error_dict = dict()

    if REQUEST_METHOD == "REST":
        request_function = request_REST
    elif REQUEST_METHOD == "gRPC":
        request_function = request_gRPC
    else:
        print("Request Method not supported!")
        return

    work_model = model
    exit()

    number_of_groups = len(services_group)
    pool = ThreadPoolExecutor(number_of_groups)

    futures = list()

    for group in services_group:
        futures.append(pool.submit(external_service, group, request_function))

    wait(futures)

    for x in as_completed(futures):
        if x.result()[0]:
            service_error_dict.update(x.result()[1])

    wait(futures)
    print("--------> Threads Done!")
    return service_error_dict


my_service_mesh = [{"seq_len": 2, "services": ["s1", "s3"]}, {"seq_len": 2, "services": ["s2"]}]

work_model_test = {
   "s0":{
      "internal_service":{
         "colosseum":{

         }
      },
      "url":"http://s0.default.svc.cluster.local",
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
      "url":"http://s1.default.svc.cluster.local",
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
      "url":"http://s2.default.svc.cluster.local",
      "path":"/api/v1",
      "image":"lucapetrucci/microservice:latest",
      "namespace":"default"
   }
}

# init_gRPC(my_service_mesh)
# exit()
# run_external_service_REST(my_service_mesh, work_model_test)
