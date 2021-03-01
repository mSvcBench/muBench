from concurrent.futures import ThreadPoolExecutor
import sched
import time
from TimingError import TimingError
import requests
import json
from pprint import pprint


microServiceSimulator_access_gateway = "http://localhost:9999"
# microServiceSimulator_access_gateway = "http://n1:31113"
workload_file_path = "workload.json"
start_time = 0.0

def richiesto_le_teste(event):
    # pprint(workload[event]["services"])
    for services in event["services"]:
        print(services)
        try:
            r = requests.get(f"{microServiceSimulator_access_gateway}/{services}")
            print(r)
        except Exception as err:
            print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event):
    try:
        worker = (v_pool.submit(richiesto_le_teste, event))
        time.sleep(0.0001)  # serve a lsciare il tempo di cambiare la variabile _state
        # print(f"{v_time}-{worker._state}-{time.time()}")
        print(f"{event['time']} - {worker._state} - Diff: {time.time()-start_time-event['time']}")
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
    with open(workload_file_path) as f:
        workload = json.load(f)
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
