from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import sched
import time
from TimingError import TimingError
import requests
import json
import sys
import os
from pprint import pprint


RUNNER_PATH = os.path.dirname(__file__)
last_print_time_ms = 0
requests_processed = 0

try:
    with open(f'{RUNNER_PATH}/RunnerParameters.json') as f:
        params = json.load(f)
    runner_parameters = params['RunnerParameters']
    ms_access_gateway = runner_parameters["ms_access_gateway"]
    workloads = runner_parameters["workload_files_path_list"]
    threads = runner_parameters["thread_pool_size"]
    round = runner_parameters["workload_rounds"]  # number of repetition rounds

except Exception as err:
    print("ERROR: in Runner,", err)
    exit(1)

stats = list()
start_time = 0.0

def do_requests(event, stats):
    global requests_processed, last_print_time_ms
    # pprint(workload[event]["services"])
    # for services in event["services"]:
        # print(services)
    requests_processed = requests_processed + 1    
    try:
        now_ms = time.time_ns() // 1_000_000
        if now_ms > last_print_time_ms + 10_000:
            print(f"Processed requests {requests_processed} \n")
            last_print_time_ms = now_ms
        r = requests.get(f"{ms_access_gateway}/{event['service']}")
        req_latency = r.elapsed.total_seconds()
        stats.append(f"{now_ms} \t {req_latency}")
        return event['time'], req_latency
    except Exception as err:
        print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event, stats):
    try:
        worker = v_pool.submit(do_requests, event, stats)
        # Wait for the thread state change
        time.sleep(0.0001)
        #  If thread status is PENDING i can not respect the timing requirements
        if worker._state == "PENDING":
            raise TimingError(event['time'])
        v_futures.append(worker)
    except TimingError as err:
        print("Error: %s" % err)


def runner(workload=None):
    global start_time, stats

    print("###############################################")
    print("############   Run Forrest Run!!   ############")
    print("###############################################")
    if len(sys.argv) > 1 and workload is None:
        workload_file = sys.argv[1]
    else:
        workload_file = workload

    with open(workload_file) as f:
        workload = json.load(f)
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(threads)
    futures = list()
    for event in workload:
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
with open("result.txt", "w") as f:
    f.writelines("\n".join(stats))
