# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
from threading import Thread
from flask import Flask, make_response
from flask import json
import traceback
from InternalJobExecutor import run_internal_job
from ExternalJobExecutor import run_external_jobs_REST
import sys
# from MicroServiceCellAbstraction.ExternalJobExecutorClass import *
import random
import os
from pprint import pprint


# try:
#     filepath = "/etc/podinfo/labels"
#     with open(filepath) as fp:
#        line = fp.readline()
#        cnt = 1
#        while line:
#            print(line)
#            if line.startswith("app="):
#                ID = line[4:].strip("\n").strip('"')
#                break
#            line = fp.readline()
#            cnt += 1
# except Exception as err:
#     print("ERROR: in read ID from app label")


def read_config_files():
    with open('/etc/MSconfig/servicemesh') as f:
        servicemesh = json.load(f)

    with open('/etc/MSconfig/workmodel') as f:
        workmodel = json.load(f)

    return servicemesh, workmodel


# Configuration Variable
# ID = "s0"  # Service ID
ID = os.environ["APP"]
service_mesh, work_model = read_config_files()
my_service_mesh = service_mesh[ID]
my_work_model = work_model[ID]

REQUEST_METHOD = "REST"

# Flask settings
flask_host = "0.0.0.0"
flask_port = 8080  # application port


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
        # return json.dumps("Update Function Not Implemented Yet! :("), 200
        return json.dumps("Successfully Update ServiceMesh and WorkModel variables! :)"), 200

    # work_model modificare in my_work_model
    @app.route(f"{my_work_model['path']}", methods=['GET'])
    def start_worker():
        try:
            HttpThread.app.logger.info('Request Received')

            # Execute the internal job
            print("*************** INTERNAL JOB STARTED ***************")
            body = run_internal_job(my_work_model["params"])
            print("############### INTERNAL JOB FINISHED! ###############")

            # Execute the external jobs
            print("*************** EXTERNAL JOB STARTED ***************")
            if len(my_service_mesh) > 0:
                service_error_dict = external_jobs(my_service_mesh, work_model)
                pprint(service_error_dict)
                if len(service_error_dict):
                    HttpThread.app.logger.error("Error in request external services")
                    HttpThread.app.logger.error(service_error_dict)
                    return make_response(json.dumps({"message": "Error in same external services request"}), 500)
            print("############### EXTERNAL JOB FINISHED! ###############")

            response = make_response(body)
            response.mimetype = "text/plain"
            return response
            # return json.dumps(body), 200
            # return json.dumps(service_mesh[ID]), 200
        except Exception as err:
            print(traceback.format_exc())
            return json.dumps({"message": "Error"}), 500


if __name__ == '__main__':

    if REQUEST_METHOD == "REST":
        # Function association
        external_jobs = run_external_jobs_REST
    else:
        print("Error: Unsupported request method")
        sys.exit(0)

    # Function
    http_thread = HttpThread()
    http_thread.start()

    http_thread.join()

