from concurrent.futures import ThreadPoolExecutor
import sched
import time
from TimingError import TimingError
import requests
import json
from pprint import pprint

# input workload.json



work_model = {"s0": {"url": "http://localhost:9999",
                     "path": "/api/v0",
                     "image": "python:latest",
                     "params": {"c": 101, "b": 11}
                     },
              "s1": {"url": "http://localhost:9999",
                     "path": "/api/v1",
                     "image": "python:latest",
                     "params": {"c": 102, "b": 12}
                     },
              "s2": {"url": "http://localhost:9999",
                     "path": "/api/v2",
                     "image": "python:latest",
                     "params": {"c": 103, "b": 13}
                     },
              "s3": {"url": "http://localhost:9999",
                     "path": "/api/v3",
                     "image": "python:latest",
                     "params": {"c": 104, "b": 14}
                     },
              "s4": {"url": "http://localhost:9999",
                     "path": "/api/v4",
                     "image": "python:latest",
                     "params": {"c": 105, "b": 15}
                     }
              }

# Il runner ha un threadPool che esegue le varie richieste
# Workload = [{"time": t0, "services":[{"sx": "p"}, {"sx": "p"}, ...]}, ...]
workload = [{'services': {'s0': 1, 's2': 0.8}, 'time': 0},
            {'services': {'s1': 1, 's2': 0.8, 's4': 0.5}, 'time': 0},
            {'services': {'s2': 0.8}, 'time': 0},
            {'services': {'s3': 0.3, "s4": 0.5}, 'time': 10},
            {'services': {'s1': 1}, 'time': 15}]

# Non mi serve piu', il runner non sta dentro il cluster
# def read_config_files():
#     with open('/etc/MSconfig/workload') as f:
#         v_workload = json.load(f)
#     # v_workload = ""
#     with open('/etc/MSconfig/workmodel') as f:
#         workmodel = json.load(f)
#
#     return v_workload, workmodel
#
# workload, work_model = read_config_files()

start_time = 0.0


def richiesto_le_teste(event):
    # pprint(workload[event]["services"])
    for services in event["services"]:
        print(services)
        try:
            r = requests.get(f"http://n1:31113/{services}")
            print(r)
        except Exception as err:
            print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event):
    try:
        worker = (v_pool.submit(richiesto_le_teste, event))
        time.sleep(0.0001)  # serve a lsciare il tempo di cambiare la variabile _state
        # print(f"{v_time}-{worker._state}-{time.time()}")
        print(f"{event['time']} - {worker._state} - Diff: {time.time()-start_time}")
        # Se il thread viene messo in pending significa che non ho thread liberi e quindi non rispetto
        # i tempi per le richieste
        if worker._state == "PENDING":
            raise TimingError(event['time'])
        v_futures.append(worker)
    except TimingError as err:
        print("Error: %s" % err)


def runner():
    global start_time
    print("I am THE Runner!!")
    # pprint(workload)
    # pprint(work_model)
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(2)
    futures = list()
    # print("Time_1:", time.time()*1000)
    # events = [10, 20, 30, 40, 50, 100, 150]
    # events = [0, 1, 2, 3, 4, 5, 10, 15]
    # for event_time in events:
    for event in workload:
        # s.enter(event_time, 1, job_assignment, argument=(pool, futures, event_time))
        s.enter(event["time"], 1, job_assignment, argument=(pool, futures, event))

    start_time = time.time()
    print("Time_1:", start_time)
    s.run()


runner()
