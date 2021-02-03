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
# from MicroServiceAbstraction.ExternalJobExecutorClass import *
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
    with open('/etc/config/mesh') as f:
        mesh = json.load(f)

    with open('/etc/config/model') as f:
        model = json.load(f)

    return mesh, model


# Configuration Variable
# ID = "s1"  # Service ID
ID = os.environ["APP"]
service_mesh, work_model = read_config_files()
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
        return json.dumps("Update Function Not Implemented Yet! :("), 200


    @app.route(f"{work_model[ID]['path']}", methods=['GET'])
    def start_worker():
        try:
            HttpThread.app.logger.info('Request Received')

            # Execute the internal job
            print("*************** INTERNAL JOB STARTED ***************")
            run_internal_job(work_model[ID]["params"])
            print("############### INTERNAL JOB FINISHED! ###############")

            # Execute the external jobs
            print("*************** EXTERNAL JOB STARTED ***************")
            if len(service_mesh[ID]) > 0:
                service_error_dict = external_jobs(service_mesh[ID], work_model)
                pprint(service_error_dict)
                if len(service_error_dict):
                    HttpThread.app.logger.error("Error in request external services")
                    HttpThread.app.logger.error(service_error_dict)
                    return make_response(json.dumps({"message": "Error in same external services request"}), 500)
            print("############### EXTERNAL JOB FINISHED! ###############")
            # Make response with size E[Y] = B
            # KB -> 1024**1
            # MB -> 1024**2
            # GB -> 1024**3
            bandwidth_load = random.expovariate(1/work_model[ID]["params"]["b"])
            print("E[bandwidth] = 1/%d ---> Response size = %d KB" % (work_model[ID]["params"]["b"], bandwidth_load))
            num_chars = 1024 * bandwidth_load  # Response in KB
            body = 'L' * int(num_chars)
            return make_response(body)
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

