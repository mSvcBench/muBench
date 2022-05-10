# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import json
import os
import sys
import time
import traceback
import logging
from threading import Thread
from concurrent import futures
from multiprocessing import Array, Manager, Value
from pprint import pprint

import gunicorn.app.base
from flask import Flask, Response, json, make_response, request
import prometheus_client
from prometheus_client import CollectorRegistry, Summary, multiprocess

from ExternalServiceExecutor import init_REST, init_gRPC, run_external_service
from InternalServiceExecutor import run_internal_service

import mub_pb2_grpc as pb2_grpc
import mub_pb2 as pb2
import grpc


# Configuration of global variables

def read_config_files():
    with open('MSConfig/workmodel.json') as f:
        workmodel = json.load(f)
    return workmodel

ID = os.environ["APP"]
ZONE = os.environ["ZONE"]  # Pod Zone
K8S_APP = os.environ["K8S_APP"]  # K8s label app
PN = os.environ["PN"] # Number of processes
TN = os.environ["TN"] # Number of thread per process

globalDict=Manager().dict()
globalDict['work_model'] = read_config_files()    # must be shared among processes for hot update
my_service_mesh = globalDict['work_model'][ID]['external_services'] # must be shared among processes for hot update
my_work_model = globalDict['work_model'][ID] # must be shared among processes for hot update

if "request_method" in my_work_model.keys():
    request_method = my_work_model["request_method"].lower()
else:
    request_method = "rest"

########################### PROMETHEUS METRICS
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
RESPONSE_SIZE = Summary('mub_response_size', 'Response size',
                        ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service'], registry=registry
                        )
INTERNAL_PROCESSING = Summary('mub_internal_processing_latency_seconds', 'Latency of internal service',
                           ['zone', 'app_name', 'method', 'endpoint'],registry=registry
                           )
EXTERNAL_PROCESSING = Summary('mub_external_processing_latency_seconds', 'Latency of external services',
                           ['zone', 'app_name', 'method', 'endpoint'], registry=registry
                           )
REQUEST_PROCESSING = Summary('mub_request_processing_latency_seconds', 'Request latency including external and internal service',
                           ['zone', 'app_name', 'method', 'endpoint', 'from', 'kubernetes_service'],registry=registry
                           )

# Flask APP
app = Flask(__name__)

@app.route("/update", methods=['GET'])
def update():
    print("updatePath")
    global globalDict
    globalDict['work_model'] = read_config_files() 
    return f'{json.dumps("Successfully Update ServiceMesh and WorkModel variables! :)")}\n', 200

@app.route(f"{my_work_model['path']}", methods=['GET'])
def start_worker():
    global globalDict
    work_model = globalDict['work_model']
    my_service_mesh = globalDict['work_model'][ID]['external_services'] # must be shared among processes for hot update
    my_work_model = globalDict['work_model'][ID] # must be shared among processes for hot update
    
    try:
        start_request_processing = time.time()
        app.logger.info('Request Received')

        # Execute the internal service
        print("*************** INTERNAL SERVICE STARTED ***************")
        start_local_processing = time.time()
        body = run_internal_service(my_work_model["internal_service"])
        local_processing_latency = time.time() - start_local_processing
        INTERNAL_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path).observe(local_processing_latency)
        RESPONSE_SIZE.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(len(body))
        print("len(body): %d" % len(body))
        print("############### INTERNAL SERVICE FINISHED! ###############")

        # Execute the external services
        start_external_request_processing = time.time()
        print("*************** EXTERNAL SERVICES STARTED ***************")
        if len(my_service_mesh) > 0:
            service_error_dict = run_external_service(my_service_mesh, work_model)
            if len(service_error_dict):
                pprint(service_error_dict)
                app.logger.error("Error in request external services")
                app.logger.error(service_error_dict)
                return make_response(json.dumps({"message": "Error in same external services request"}), 500)
        print("############### EXTERNAL SERVICES FINISHED! ###############")

        response = make_response(body)
        response.mimetype = "text/plain"
        EXTERNAL_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path).observe(time.time() - start_external_request_processing)
        REQUEST_PROCESSING.labels(ZONE, K8S_APP, request.method, request.path, request.remote_addr, ID).observe(time.time() - start_request_processing)

        return response
    except Exception as err:
        print(traceback.format_exc())
        return json.dumps({"message": "Error"}), 500

# Prometheus
@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

# Custom Gunicorn application: https://docs.gunicorn.org/en/stable/custom.html
class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

# GRPC (no multi-process)
gRPC_port = 51313
class gRPCThread(Thread, pb2_grpc.MicroServiceServicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(TN)))

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
            INTERNAL_PROCESSING.labels(ZONE, K8S_APP, "grpc", "grpc").observe(local_processing_latency)
            RESPONSE_SIZE.labels(ZONE, K8S_APP, "grpc", "grpc", remote_address, ID).observe(len(body))
            print("len(body): %d" % len(body))
            print("############### INTERNAL SERVICE FINISHED! ###############")

            # Execute the external services
            print("*************** EXTERNAL SERVICES STARTED ***************")
            start_external_request_processing = time.time()
            if len(my_service_mesh) > 0:
                service_error_dict = run_external_service(my_service_mesh, globalDict['work_model'])
                if len(service_error_dict):
                    pprint(service_error_dict)
                    logging.error("Error in request external services")
                    logging.error(service_error_dict)
                    result = {'text': f"Error in same external services request", 'status_code': False}
                    return pb2.MessageResponse(**result)
            print("############### EXTERNAL SERVICES FINISHED! ###############")

            result = {'text': body, 'status_code': True}
            EXTERNAL_PROCESSING.labels(ZONE, K8S_APP, "grpc", "grpc").observe(time.time() - start_external_request_processing)
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
    global data
    if request_method == "rest":
        init_REST()
        # Start Gunicorn HTTP REST Server (multi-process)
        options_gunicorn = {
            'bind': '%s:%s' % ('0.0.0.0', 8080),
            'workers': PN,
            'config': "/app/gunicorn.conf.py",
            'threads':TN
        }
        HttpServer(app, options_gunicorn).run()
    elif request_method == "grpc":
        init_gRPC(my_service_mesh, globalDict['work_model'], gRPC_port)
        # Start the gRPC server
        grpc_thread = gRPCThread()
        grpc_thread.run()
        # Flask HTTP REST server started for Prometheus metrics and for the entry point (s0) that anyway receives REST requests from API gateway
        app.run(host='0.0.0.0', port=8080, threaded=True)
    else:
        print("Error: Unsupported request method")
        sys.exit(0)


