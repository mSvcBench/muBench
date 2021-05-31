from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import sched
import time
from TimingError import TimingError
import requests
import json
import sys
from datetime import datetime
from pprint import pprint

ms_access_gateway = "http://160.80.103.216:31113"
workloads = ["/Users/detti/Documents/MyDocuments/Personali/Prin2018/MicroServiceSimulator/WorkLoadGenerator/workload_test500.json"]
stats = list()
start_time = 0.0

def do_requests(event, stats):
    # pprint(workload[event]["services"])
    # for services in event["services"]:
        # print(services)
    try:
        now = time.time() * 1000
        r = requests.get(f"{ms_access_gateway}/{event['service']}")
        req_latency = r.elapsed.total_seconds()
        stats.append(f"{now} \t {req_latency}") 
        return event['time'], req_latency
    except Exception as err:
        print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event, stats):
    try:
        worker = v_pool.submit(do_requests, event, stats)
        time.sleep(0.0001)  # lascia il tempo di cambiare la variabile _state
        # print(f"{v_time}-{worker._state}-{time.time()}")
        # print(f"{event['time']} - {worker._state} - Delay: {time.time()/1000-start_time-event['time']}")
        # Se il thread viene messo in pending significa che non ho thread liberi e quindi non rispetto
        # i tempi per le richieste
        if worker._state == "PENDING":
            raise TimingError(event['time'])
        v_futures.append(worker)
    except TimingError as err:
        print("Error: %s" % err)


def runner(workload=None):
    global start_time, stats

    # print("I am THE Runner!!")
    print("###############################################")
    print("############   Run Forrest Run!!   ############")
    print("###############################################")
    if len(sys.argv) > 1 and workload is None:
        workload_file = sys.argv[1]
    else:
        workload_file = workload

    with open(workload_file) as f:
        workload = json.load(f)
    # pprint(workload)
    # pprint(work_model)
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(100)
    futures = list()
    # print("Time_1:", time.time()*1000)
    # events = [10, 20, 30, 40, 50, 100, 150]
    # events = [0, 1, 2, 3, 4, 5, 10, 15]
    # for event_time in events:
    for event in workload:
        # s.enter(event_time, 1, job_assignment, argument=(pool, futures, event_time))
        # in seconds
        # s.enter(event["time"], 1, job_assignment, argument=(pool, futures, event))
        # in milliseconds
        s.enter((event["time"]/1000+2), 1, job_assignment, argument=(pool, futures, event, stats))


    start_time = time.time()
    print("Start Time:", datetime.now().strftime("%H:%M:%S.%f - %g/%m/%Y"))
    s.run()

    wait(futures)
    print("###############################################")
    print("###########   Stop Forrest Stop!!   ###########")
    print("###############################################")
    print("Run Duration (sec): %.6f" % (time.time() - start_time))




round = 1 # number of repetition rounds
for cnt, workload_var in enumerate(workloads):
    for x in range(round):
        print("Round: %d -- workload: %s" % (x+1, workload_var))
        runner(workload_var)
        print("***************************************")
    #     if cnt != len(workloads) - 1 or x != round - 1:
    #         print("Sleep for 240 sec")
    #         time.sleep(240)
    # if cnt != len(workloads) - 1:
    #     print("Sleep for 240 sec")
    #     time.sleep(240)
with open("result.txt","w") as f:
    f.write(stats)
