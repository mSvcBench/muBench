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
from MicroServiceAbstraction.InternalJobExecutor import run_internal_job
from MicroServiceAbstraction.ExternalJobExecutor import run_external_jobs_REST
import random

# Only for TEST
service_mesh = {"s1": [{"seq_len": 3,
                        "services": ["s2", "s3", "s5"]
                        },
                        {"seq_len": 2,
                        "services": ["s5", "sLuca"]
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
WORK_MODEL = {"s1": {"url": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 5}
                     },
              "s2": {"url": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 6}
                     }
              }

ID = "s1"  # Service ID

# WORK_MODEL = {"c": 5, "b": 10}
REQUEST_METHOD = "REST"

# Flask settings
flask_host = "0.0.0.0"
flask_port = 8080  # application port

# Requests in python
# req = requests.get(uri, headers=new_headers, stream=True)
# response_headers = dict(req.headers)


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

    # PATH BRUTTO E NOME FUNZIONE BRUTTO
    @app.route(f"{WORK_MODEL[ID]['url']}", methods=['GET'])
    def start_worker():
        try:
            HttpThread.app.logger.info('request received')
            # Inutile solo per fare alcuni test sulla questione multi-thread
            # param = request.args.get('p')

            # Execute the internal job
            print("*************** INTERNAL JOB ***************")
            run_internal_job(WORK_MODEL[ID]["params"])
            print("*************** INTERNAL JOB FINISHED! ***************")

            # Execute the external jobs
            print("*************** EXTERNAL JOB ***************")
            if len(service_mesh[ID]) > 0:
                external_jobs(service_mesh[ID])
            print("*************** EXTERNAL JOB FINISHED! ***************")

            # Make response with size E[Y] = B
            # KB -> 1024**1
            # MB -> 1024**2
            # GB -> 1024**3
            bandwidth_load = random.expovariate(1/WORK_MODEL[ID]["params"]["b"])
            num_chars = 1024 * bandwidth_load
            body = '0' * int(num_chars)
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
    # TODO
    # try:
    #     http_thread = HttpThread()
    #     http_thread.start()
    # except KeyboardInterrupt:
    #     print('^C received, shutting down the web server')


