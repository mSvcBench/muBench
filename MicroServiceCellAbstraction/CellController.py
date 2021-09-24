# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
from threading import Thread
from flask import Flask, make_response, json, request
import traceback
from InternalServiceExecutor import run_internal_service
from ExternalServiceExecutor import run_external_service, init_gRPC, init_REST
import sys
import random
import os
from pprint import pprint
from prometheus_client import start_http_server, Gauge, Counter, Histogram, Summary
import time

import mub_pb2_grpc as pb2_grpc
import mub_pb2 as pb2
import grpc
from concurrent import futures


def read_config_files():

    with open('MSConfig/workmodel.json') as f:
        workmodel = json.load(f)

    return workmodel


# Configuration Variable
ID = os.environ["APP"]
ZONE = os.environ["ZONE"]  # Pod Zone
K8S_APP = os.environ["K8S_APP"]  # K8s label app
work_model = read_config_files()
my_service_mesh = work_model[ID]['external_services']
my_work_model = work_model[ID]
if "request_method" in my_work_model.keys():
    request_method = my_work_model["request_method"].lower()
else:
    request_method = "rest"


########################### PROMETHEUS METRICS
REQUEST_LATENCY = Summary('mub_request_latency_seconds', 'Request latency',
                          ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service']
                          )

RESPONSE_SIZE = Summary('mub_response_size', 'Response size',
                        ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service']
                        )

LOCAL_PROCESSING = Summary('mub_local_processing_latency_seconds', 'Local processing latency',
                           ['zone', 'app_name', 'method', 'endpoint']
                           )

REQUEST_PROCESSING = Summary('mub_request_processing_seconds', 'Request latency without the network latency',
                           ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service']
                           )

def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = time.time() - request.start_time
    # REQUEST_LATENCY.labels('mss', request.path, request.remote_addr).observe(resp_time)
    REQUEST_LATENCY.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(resp_time)
    return response

# Flask settings
flask_host = "0.0.0.0"
flask_port = 8080  # application port

gRPC_port = 51313

class HttpThread(Thread):
    app = Flask(__name__)

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print("Thread http started")
        global flask_host, flask_port

        logging.basicConfig(level=logging.INFO)

        self.app.run(host=flask_host, port=flask_port)
        print("Thread '" + self.name + "closed")

    @app.route("/update", methods=['GET'])
    def update():
        print("updatePath")
        global work_model, my_work_model, my_service_mesh
        work_model = read_config_files()
        my_service_mesh = work_model[ID]['external_services']
        my_work_model = work_model[ID]
        return f'{json.dumps("Successfully Update ServiceMesh and WorkModel variables! :)")}\n', 200

    @app.route(f"{my_work_model['path']}", methods=['GET'])
    def start_worker():
        try:
            start_request_processing = time.time()
            HttpThread.app.logger.info('Request Received')

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
                if len(service_error_dict):
                    pprint(service_error_dict)
                    HttpThread.app.logger.error("Error in request external services")
                    HttpThread.app.logger.error(service_error_dict)
                    return make_response(json.dumps({"message": "Error in same external services request"}), 500)
            print("############### EXTERNAL SERVICES FINISHED! ###############")

            response = make_response(body)
            response.mimetype = "text/plain"
            REQUEST_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(time.time() - start_request_processing)

            return response
        except Exception as err:
            print(traceback.format_exc())
            return json.dumps({"message": "Error"}), 500


class gRPCThread(Thread, pb2_grpc.MicroServiceServicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def __init__(self):
        Thread.__init__(self)

    def GetMicroServiceResponse(self, req, context):
        try:
            start_request_processing = time.time()
            logging.info('Request Received')
            message = req.message
            remote_address = context.peer().split(":")[1]
            print(f'I am service: {ID} and I received this message: --> "{message}"')

            # Execute the internal service
            print("*************** INTERNAL SERVICE STARTED ***************")
            start_local_processing = time.time()
            body = run_internal_service(my_work_model["internal_service"])
            local_processing_latency = time.time() - start_local_processing
            LOCAL_PROCESSING.labels(ZONE, K8S_APP, "grpc", "grpc").observe(local_processing_latency)
            RESPONSE_SIZE.labels(ZONE, K8S_APP, "grpc", "grpc", remote_address, ID).observe(len(body))
            print("len(body): %d" % len(body))
            print("############### INTERNAL SERVICE FINISHED! ###############")

            # Execute the external services
            print("*************** EXTERNAL SERVICES STARTED ***************")
            if len(my_service_mesh) > 0:
                service_error_dict = run_external_service(my_service_mesh, work_model)
                if len(service_error_dict):
                    pprint(service_error_dict)
                    logging.error("Error in request external services")
                    logging.error(service_error_dict)
                    result = {'text': f"Error in same external services request", 'status_code': False}
                    return pb2.MessageResponse(**result)
            print("############### EXTERNAL SERVICES FINISHED! ###############")

            result = {'text': body, 'status_code': True}
            REQUEST_PROCESSING.labels(ZONE, K8S_APP, "grpc", "grpc", remote_address, ID).observe(
                time.time() - start_request_processing)
            return pb2.MessageResponse(**result)
        except Exception as err:
            print("Error: in GetMicroServiceResponse,", err)
            result = {'text': f"Error: in GetMicroServiceResponse, {str(err)}", 'status_code': False}
            return pb2.MessageResponse(**result)

    def run(self):
        pb2_grpc.add_MicroServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port(f'[::]:{gRPC_port}')
        self.server.start()


if __name__ == '__main__':

    if request_method == "rest":
        init_REST()

    elif request_method == "grpc":
        init_gRPC(my_service_mesh, work_model, gRPC_port)
        # Start the gRPC server threads
        grpc_thread = gRPCThread()
        grpc_thread.run()
    else:
        print("Error: Unsupported request method")
        sys.exit(0)

    # Function
    # If mode is gRPC the http thread is necessary for the entry point (s0) that receive a REST request
    http_thread = HttpThread()

    # Metrics configuration (REQUEST_LATENCY)
    http_thread.app.before_request(start_timer)
    # http_thread.app.after_request(record_request_data)
    http_thread.app.after_request(stop_timer)

    http_thread.start()

    # Prometheus thread
    start_http_server(8081)

    http_thread.join()
