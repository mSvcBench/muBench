import random
from readline import append_history_file
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import time
import grpc
import mub_pb2_grpc as pb2_grpc
import mub_pb2 as pb2
import json
from pprint import pprint


service_stub = dict()
s = requests.Session()

def init_REST(app):
    app.logger.info("Init REST function")
    global request_function
    request_function = request_REST

# TODO 
def init_gRPC(my_service_graph, workmodel, server_port, app):
    app.logger.info("Init gRPC function")
    global service_stub, request_function
    request_function = request_gRPC

    for group in my_service_graph:
        for service in group["services"]:
            host = f'{workmodel[service]["url"]}'
            # instantiate a channel
            channel = grpc.insecure_channel(
                '{}:{}'.format(host, server_port))
            # bind the client and the server
            service_stub[service] = pb2_grpc.MicroServiceStub(channel)


# return the size of the body, NOT the body
def build_post_request_body(params, trace_size_to_send=0):
    """
    Builds the body of a POST request based on the given parameters.
    Args:
        params (dict): A dictionary containing the parameters for the request.
            - "request_dist" (str): The distribution type of the request size, either "const" or "exp".
            - "request_size" (int): The size of the request in kB.
        trace_size_to_send (int, optional): present if TRACEDRIVEN test -> The size of the trace to send to the next service, 
                                                this is subtracted from the size of the generated request. Default value 0

    Returns:
        str: The body of the POST request as a string of characters. If the calculated number of characters is less than 1, returns an empty string.

    Raises:
        Exception: If there is an error during the construction of the request body.
    """
    try:
        if params["request_dist"] == "const":
            num_chars = 1000 * int(params["request_size"] - trace_size_to_send) # Response in kB
            # request_body = 'V' * num_char # Response in kB
            # return request_body
        elif params["request_dist"] == "exp":            
            bandwidth_load = random.expovariate(1 / params["request_size"])
            num_chars = int(max(1, 1000 * bandwidth_load - trace_size_to_send))  # Response in kB
            # request_body = 'F' * num_chars
            # return request_body
        
        if num_chars < 1:
            return ""
        request_body = 'M' * int(num_chars) # Response in kB
        return request_body
    except Exception as err:
        raise Exception(f"Error in 'build_post_request_body' {err}")

def request_REST(service,id,work_model,s,trace,query_string, app, jaeger_context):
    try:
        service_no_escape = service.split("__")[0]
        if len(trace)==0 and len(query_string)==0:
            # default
            request_method = work_model[service_no_escape].get("request_method", "").lower()
            if request_method == "post":
                request_parameters = work_model[service_no_escape]["request_parameters"]
                request_body = build_post_request_body(request_parameters)
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'request-type': 'iot'}
                headers.update(jaeger_context)
                json_payload = json.dumps(request_body)
                return s.post(f'http://{work_model[service_no_escape]["url"]}{work_model[service_no_escape]["path"]}',data=json_payload,headers=headers)
            
            else:
                return s.get(f'http://{work_model[service_no_escape]["url"]}{work_model[service_no_escape]["path"]}', headers=jaeger_context)
        elif len(trace)>0:
            # trace-driven request
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'request-type': 'tracedriven'}
            headers.update(jaeger_context)
            json_dict = dict()
            json_dict[service] = trace[id][service]
            request_parameters = work_model[service_no_escape]["request_parameters"]
            json_dict["dummy"] = build_post_request_body(request_parameters, len(json_dict[service]))
            json_payload = json.dumps(json_dict)
            if  len(query_string)==0:
                return s.post(f'http://{work_model[service_no_escape]["url"]}{work_model[service_no_escape]["path"]}',data=json_payload,headers=headers)
            else:
                return s.post(f'http://{work_model[service_no_escape]["url"]}{work_model[service_no_escape]["path"]}?{query_string}',data=json_payload,headers=headers)
        elif  len(query_string)>0:
            # request with enclosed behaviour information
            return s.get(f'http://{work_model[service_no_escape]["url"]}{work_model[service_no_escape]["path"]}?{query_string}', headers=jaeger_context)  
        else:
            r = requests.Response()
            r.status_code = 505
            return r
    except Exception as err:
        app.logger.error("Error in request external service %s -- %s" % (service, str(err)))
        r = requests.Response()
        r.status_code = 505
        return r

def request_gRPC(service,id,work_model,s,trace,query_string,app, trace_context=None):
    message = pb2.Message(message=f"Hello service: {service}")
    # app.logger.info(f'{message}')
    response = service_stub[service].GetMicroServiceResponse(message)
    return response


def external_service(group,id,work_model,trace,query_string, app, trace_context):
    app.logger.info("**** Start SERVICES in thread: %s" % str(group))
    global request_function
    if group["seq_len"] < len(group["services"]):
        # Randomly select seq_len elements from services in the group
        selected_services = random.sample(group["services"], k=group["seq_len"])
    else:
        selected_services = group["services"]

    # read probabilities of services of the group, if exist
    if "probabilities" in  group.keys():
        probabilities = group["probabilities"]
    else:
        probabilities = dict()
    
    service_error_dict = dict()
    service_error_flag = False

    for service in selected_services:
        # sleep_time = random.randint(2, 5)
        # app.logger.info("**** Service: %s -- Sleep for %d" % (service, sleep_time))
        # time.sleep(sleep_time)
        try:
            # "url": "http://s0.default.svc.cluster.local",
            # "path": "/api/v1",
            if service in probabilities.keys():
                p = probabilities[service]
            else:
                p = 1
            if random.random() < p :
                # service called with probability p
                r = request_function(service,id,work_model,s,trace,query_string, app, trace_context)
                app.logger.info("Service: %s -> Status_code: %s -- len(text): %d" % (service, r.status_code, len(r.text)))
                if type(r.status_code) == bool and not r.status_code:
                    raise Exception(f"Error in external service: {service} -- (gRPC) status_code: {r.status_code}")
                elif type(r.status_code) == int and r.status_code != 200:
                    raise Exception(f"Error in external service: {service} -- (REST) status_code: {r.status_code}")

        except Exception as err:
            service_error_dict[service] = err
            service_error_flag = True
            app.logger.error("Error in request external service %s -- %s" % (service, str(err)))

    app.logger.info("#### SERVICE Done!")
    return service_error_flag, service_error_dict


def run_external_service(services_group, work_model, query_string, trace, app, trace_context=None):
    
    app.logger.info("** EXTERNAL SERVICES")
    service_error_dict = dict()
    number_of_groups = len(services_group)
    pool = ThreadPoolExecutor(number_of_groups)
    futures = list()
    id = 0
    for group in services_group:
        futures.append(pool.submit(external_service, group, id, work_model, trace, query_string, app, trace_context))
        id = id + 1
    wait(futures)
    for x in as_completed(futures):
        if x.result()[0]:
            service_error_dict.update(x.result()[1])
    app.logger.info("--------> Threads Done!")
    return service_error_dict