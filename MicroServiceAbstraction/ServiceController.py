# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import logging
from threading import Thread
from flask import Flask, make_response
from flask import Response
from flask import json
import sys
import traceback
import time
from InternalJobExecutor import run_internal_job
from ExternalJobExecutor import run_external_jobs_REST
import sys
# from MicroServiceAbstraction.ExternalJobExecutorClass import *
import random
from pprint import pprint
import os
import TestVar as TsVar

'''
# Only for TEST
service_mesh = {"s1": [{"seq_len": 3,
                        "services": ["s2", "s3"]
                        },
                        {"seq_len": 1,
                        "services": ["s3"]
                        }
                       ],
                "s2": [],
                "s3": [{"seq_len": 1,
                        "services": ["s4"]}],
                "s4": [],
                "s5": []
                }


# CPU load for t seconds -> c: exp negative with average C
# Response length  -> b: exp negative with average B
WORK_MODEL = {"s1": {"url": "http://localhost:9001",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 101, "b": 1}
                     },
              "s2": {"url": "http://localhost:9002",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 102, "b": 2}
                     },
              "s3": {"url": "http://localhost:9003",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 103, "b": 3}
                     },
              "s4": {"url": "http://localhost:9004",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 104, "b": 4}
                     },
              "s5": {"url": "http://localhost:9005",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 105, "b": 5}
                     }
              }
'''

ID = "s1"  # Service ID
# ID = sys.argv[1]  # Service ID
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

# ID = os.environ["APP"]

service_mesh = TsVar.service_mesh
WORK_MODEL = TsVar.WORK_MODEL


REQUEST_METHOD = "REST"

# Flask settings
flask_host = "0.0.0.0"
flask_port = 8080  # application port
# flask_port = WORK_MODEL[ID]["url"].split(":")[-1]  # application port


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

    @app.route(f"{WORK_MODEL[ID]['path']}", methods=['GET'])
    def start_worker():
        try:
            HttpThread.app.logger.info('request received')

            # Inutile solo per fare alcuni test sulla questione multi-thread
            # param = request.args.get('p')

            # Execute the internal job
            print("*************** INTERNAL JOB ***************")
            run_internal_job(WORK_MODEL[ID]["params"])
            print("############### INTERNAL JOB FINISHED! ###############")

            # Execute the external jobs
            print("*************** EXTERNAL JOB ***************")

            if len(service_mesh[ID]) > 0:
                service_error_dict = external_jobs(service_mesh[ID], WORK_MODEL)
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
            # bandwidth_load = 13
            bandwidth_load = random.expovariate(1/WORK_MODEL[ID]["params"]["b"])
            num_chars = 1024 * bandwidth_load
            body = 'L' * int(num_chars)
            return make_response(body)
            # return json.dumps(service_mesh[ID]), 200
            # return json.dumps({"message": "Bad username or password"}), 401
        except Exception as er:
            print(traceback.format_exc())
            return json.dumps({"message": "Error"}), 500


if __name__ == '__main__':

    # Get parameters from env
    # parameters = os.environ["LOGNAME"]
    # print("LOGNAME: %s" %parameters)

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

    # try:
    #     http_thread = HttpThread()
    #     http_thread.start()
    # except KeyboardInterrupt:
    #     print('^C received, shutting down the web server')


# import requests
# time.sleep(2)
# requests.get("http://localhost:8080/api/v1")
