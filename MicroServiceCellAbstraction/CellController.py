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
# from MicroServiceCellAbstraction.ExternalJobExecutorClass import *
import random
import os
from pprint import pprint
from prometheus_client import start_http_server, Gauge, Counter, Histogram, Summary
import time

import mss_pb2_grpc as pb2_grpc
import mss_pb2 as pb2
import grpc
from concurrent import futures


def read_config_files():
    with open('MSConfig/servicemesh.json') as f:
        servicemesh = json.load(f)

    with open('MSConfig/workmodel.json') as f:
        workmodel = json.load(f)

    return servicemesh, workmodel


# Configuration Variable
ID = "s0"  # Service ID
# ID = os.environ["APP"]
ZONE = "default"
# ZONE = os.environ["ZONE"]  # Pod Zone
K8S_APP = "s0-pod"
# K8S_APP = os.environ["K8S_APP"]  # K8s label app
service_mesh, work_model = read_config_files()
my_service_mesh = service_mesh[ID]
my_work_model = work_model[ID]

################################
# Modifico my_work_model per i test
# my_work_model["params"] = {'ave_luca': {"probability": 0.3, "ave_number": 13, "mean_bandwidth": 42}}
# my_work_model["params"] = {'compute_pi': {"probability": 1, 'mean_bandwidth': 1, 'range_complexity': [101, 101]}}
pprint(my_service_mesh)
pprint(my_work_model)
# exit()
################################

########################### PROMETHEUS METRICS

# request_latency_seconds_luca_sum/request_latency_seconds_luca_count
# histogram_quantile(0.5, rate(request_latency_seconds_luca_bucket[10m])

# Misuro la latenza media delle richieste, quindi mi memorizzo la somma dei tempi e il numero delle richieste
# Latency --> Zona_pod, app_name, method, endpoint, from      -> Sommo la latency
# Misuro il throughput quindi mi memorizzo il totale dei dati scambiati e il numero delle richieste
# Throughput --> Zona_pod, app_name, method, endpoint, from   -> Sommo il body

# Local Processing --> Misuro il tempo di esecuzione della funzione

# tutti counter
REQUEST_LATENCY = Summary('mss_request_latency_seconds', 'Request latency',
                          ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service']
                          )

RESPONSE_SIZE = Summary('mss_response_size', 'Response size',
                        ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service']
                        )

LOCAL_PROCESSING = Summary('mss_local_processing_latency_seconds', 'Local processing latency',
                           ['zone', 'app_name', 'method', 'endpoint']
                           )


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = time.time() - request.start_time
    # REQUEST_LATENCY.labels('mss', request.path, request.remote_addr).observe(resp_time)
    REQUEST_LATENCY.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(resp_time)
    return response


# def record_response_data(response):
#     REQUEST_LATENCY.labels(ZONE, 'mss', request.method, request.path, request.remote_addr).observe(body)
#     return response
############################

REQUEST_METHOD = "gRPC"

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
        global service_mesh, work_model, my_work_model, my_service_mesh
        service_mesh, work_model = read_config_files()
        my_service_mesh = service_mesh[ID]
        my_work_model = work_model[ID]
        return f'{json.dumps("Successfully Update ServiceMesh and WorkModel variables! :)")}\n', 200

    @app.route(f"{my_work_model['path']}", methods=['GET'])
    def start_worker():
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


class gRPCThread(Thread):
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

    def run(self):
        print("CIAO")
        logging.basicConfig(level=logging.INFO)

        # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_MicroServiceServicer_to_server(pb2_grpc.MicroServiceServicer(), self.server)
        self.server.add_insecure_port('[::]:51313')
        self.server.start()
        self.server.wait_for_termination()
        print(self.server)





gRPC_thread = gRPCThread()
gRPC_thread.start()


# if __name__ == '__main__':
#
#     if REQUEST_METHOD == "REST":
#         # Function association
#         init_REST()
#
#     elif REQUEST_METHOD == "gRPC":
#
#         init_gRPC(my_service_mesh, work_model)
#     else:
#         print("Error: Unsupported request method")
#         sys.exit(0)
#
#     exit()
#     mss_test_ingress = Counter('mss_test_ingress_total', 'Number of application request', ['kubernetes_service'])
#     mss_test_summary = Summary('mss_test_summary', 'Number of application request', ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service'])
#
#     # Function
#     http_thread = HttpThread()
#
#     http_thread.app.before_request(start_timer)
#     # http_thread.app.after_request(record_request_data)
#     http_thread.app.after_request(stop_timer)
#
#     http_thread.start()
#
#     # Prometheus thread
#     start_http_server(8081)
#
#     http_thread.join()

# avg((increase(mss_test_summary_sum{endpoint="/api/v1"}[2m])/increase(mss_test_summary_count{endpoint="/api/v1"}[2m])) > 0) by (kubernetes_service)

