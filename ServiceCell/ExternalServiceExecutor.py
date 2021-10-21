import random
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import time
import grpc
import mub_pb2_grpc as pb2_grpc
import mub_pb2 as pb2
from pprint import pprint


service_stub = dict()

def init_REST():
    print("Init REST function")
    global request_function
    request_function = request_REST

def init_gRPC(my_service_mesh, workmodel, server_port):
    print("Init gRPC function")
    global service_stub, request_function
    request_function = request_gRPC

    for group in my_service_mesh:
        for service in group["services"]:
            host = f'{workmodel[service]["url"]}'
            # instantiate a channel
            channel = grpc.insecure_channel(
                '{}:{}'.format(host, server_port))
            # bind the client and the server
            service_stub[service] = pb2_grpc.MicroServiceStub(channel)


def request_REST(service):
    return requests.get(f'http://{work_model[service]["url"]}{work_model[service]["path"]}')


def request_gRPC(service):
    message = pb2.Message(message=f"Hello service: {service}")
    # print(f'{message}')
    response = service_stub[service].GetMicroServiceResponse(message)
    return response


def external_service(group):
    print("**** Start SERVICES in thread: %s" % str(group))
    global request_function
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
            if type(r.status_code) == bool and not r.status_code:
                raise Exception(f"Error in request external service: {service} -- (gRPC) status_code: {r.status_code}")
            elif type(r.status_code) == int and r.status_code != 200:
                raise Exception(f"Error in request external service: {service} -- (REST) status_code: {r.status_code}")

        except Exception as err:
            service_error_dict[service] = err
            service_error_flag = True
            print("Error in request external service %s -- %s" % (service, str(err)))

    print("#### SERVICE Done!")
    return service_error_flag, service_error_dict


def run_external_service(services_group, model):
    global work_model
    print("** EXTERNAL SERVICES")
    
    service_error_dict = dict()

    work_model = model

    number_of_groups = len(services_group)
    pool = ThreadPoolExecutor(number_of_groups)

    futures = list()
    for group in services_group:
        futures.append(pool.submit(external_service, group))
    wait(futures)

    for x in as_completed(futures):
        if x.result()[0]:
            service_error_dict.update(x.result()[1])

    wait(futures)
    print("--------> Threads Done!")
    return service_error_dict
