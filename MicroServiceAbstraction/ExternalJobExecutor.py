import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
from pprint import pprint
import logging

WORK_MODEL = dict()


def external_job(group):
    print("**** Start JOBS nel thread: %s" % str(group))
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
            # s1-svc.default.service.local/%s %("api/v1")
            # r = requests.get('%s%s' % (WORK_MODEL[service]["url"], WORK_MODEL[service]["path"]))
            # r = requests.get("http://s1.default.svc.cluster.local/api/v1")
            r = requests.get(f'{WORK_MODEL[service]["url"]}{WORK_MODEL[service]["path"]}')
            print("Service: %s -> Status_code: %s -- len(text): %d" % (service, r.status_code, len(r.text)))
        except Exception as err:
            service_error_dict[service] = err
            service_error_flag = True
            print("Error in request external service %s -- %s" % (service, str(err)))


    print("#### JOB Done!")
    return service_error_flag, service_error_dict


def run_external_jobs_REST(jobs_group, work_model):
    print("** EXTERNAL JOBS")
    global WORK_MODEL
    WORK_MODEL = work_model

    number_of_groups = len(jobs_group)
    pool = ThreadPoolExecutor(number_of_groups)

    futures = list()

    for group in jobs_group:
        futures.append(pool.submit(external_job, group))

    wait(futures)

    # service_error_list = list()
    service_error_dict = dict()
    for x in as_completed(futures):
        if x.result()[0]:
            # service_error_list.append(x.result()[1])
            service_error_dict.update(x.result()[1])

    wait(futures)
    print("--------> Threads Done!")
    # pprint(service_error_list)
    # return service_error_list
    return service_error_dict



#########################   TEST  #################
'''
SERVIZIO_MESH = {"s1": [{"seq_len": 3,
                        # "services": ["s2"]
                        "services": ["s2", "s3", "s5"]
                        }],
                "s2": [],
                "s3": [{"seq_len": 1,
                        "services": ["s4"]}],
                "s4": [],
                "s5": []
                }

LAVORO_MODELLO = {"s1": {"url": "http://localhost:9001",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 1}
                     },
              "s2": {"url": "http://localhost:9002",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 2}
                     },
              "s3": {"url": "http://localhost:9003",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 3}
                     },
              "s4": {"url": "http://localhost:9004",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 4}
                     },
              "s5": {"url": "http://localhost:9005",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 100, "b": 5}
                     }
              }


asd = run_external_jobs_REST(SERVIZIO_MESH["s1"], LAVORO_MODELLO)

pprint(asd)

'''