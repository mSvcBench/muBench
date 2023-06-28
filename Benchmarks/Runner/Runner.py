from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import sched
import time
import threading
from TimingError import TimingError
import requests
import json
import sys
import os
import shutil
import importlib
from pprint import pprint

import argparse
import argcomplete



class Counter(object):
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start
    def increase(self):
        self.lock.acquire()
        try:
            self.value = self.value + 1
        finally:
            self.lock.release()
    def decrease(self):
        self.lock.acquire()
        try:
            self.value = self.value - 1
        finally:
            self.lock.release()


def do_requests(event, stats, local_latency_stats):
    global processed_requests, last_print_time_ms, error_requests, pending_requests
    # pprint(workload[event]["services"])
    # for services in event["services"]:
        # print(services)
    processed_requests.increase()    
    try:
        now_ms = time.time_ns() // 1_000_000
        if runner_type=="greedy":
            pending_requests.increase()
        
        r = requests.get(f"{ms_access_gateway}/{event['service']}")
        pending_requests.decrease()
        
        if r.status_code != 200:
            print("Response Status Code", r.status_code)
            error_requests.increase()

        req_latency_ms = int(r.elapsed.total_seconds()*1000)
        stats.append(f"{now_ms} \t {req_latency_ms} \t {r.status_code} \t {processed_requests.value} \t {pending_requests.value}")
        local_latency_stats.append(req_latency_ms)
        
        if now_ms > last_print_time_ms + 1_000:
            print(f"Processed request {processed_requests.value}, latency {req_latency_ms}, pending requests {pending_requests.value} \n")
            last_print_time_ms = now_ms
        return event['time'], req_latency_ms
    except Exception as err:
        print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event, stats, local_latency_stats):
    global timing_error_requests, pending_requests
    try:
        worker = v_pool.submit(do_requests, event, stats, local_latency_stats)
        v_futures.append(worker)
        if runner_type!="greedy":
            pending_requests.increase()
        if pending_requests.value > threads: 
            # maximum capacity of thread pool reached, request is queued (not an issue for greedy runner)
            if runner_type!="greedy":
                timing_error_requests += 1
                raise TimingError(event['time'])
    except TimingError as err:
        print("Error: %s" % err)

def file_runner(workload=None):
    global start_time, stats, local_latency_stats

    stats = list()
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
        s.enter((event["time"]/1000+2), 1, job_assignment, argument=(pool, futures, event, stats, local_latency_stats))

    start_time = time.time()
    print("Start Time:", datetime.now().strftime("%H:%M:%S.%f - %g/%m/%Y"))
    s.run()

    wait(futures)
    run_duration_sec = time.time() - start_time
    avg_latency = 1.0*sum(local_latency_stats)/len(local_latency_stats)

    print("###############################################")
    print("###########   Stop Forrest Stop!!   ###########")
    print("###############################################")
    print("Run Duration (sec): %.6f" % run_duration_sec, "Total Requests: %d - Error Request: %d - Timing Error Requests: %d - Average Latency (ms): %.6f - Request rate (req/sec) %.6f" % (len(workload), error_requests.value, timing_error_requests, avg_latency, 1.0*len(workload)/run_duration_sec))

    if run_after_workload is not None:
        args = {"run_duration_sec": run_duration_sec,
                "last_print_time_ms": last_print_time_ms,
                "requests_processed": processed_requests.value,
                "timing_error_number": timing_error_requests,
                "total_request": len(workload),
                "error_request": error_requests.value,
                "runner_results_file": f"{output_path}/{result_file}_{workload_var.split('/')[-1].split('.')[0]}.txt"
                }
        run_after_workload(args)

def greedy_runner():
    global start_time, stats, local_latency_stats, runner_parameters

    if 'ingress_service' in runner_parameters.keys():
        srv=runner_parameters['ingress_service']
    else:
        srv = 's0'

    stats = list()
    print("###############################################")
    print("############   Run Forrest Run!!   ############")
    print("###############################################")
    
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(threads)
    futures = list()
    event={'service':srv,'time':0}
    slow_start_end = 32 # number requests with initial delays
    slow_start_delay = 0.1
    # put every request in the thread pool scheduled at time 0 (in case with initial slow start spread to reduce initial concurrency)
    for i in range(workload_events):
        if i < slow_start_end :
            event_time =  i * slow_start_delay
        s.enter(event_time, 1, job_assignment, argument=(pool, futures, event, stats, local_latency_stats))

    start_time = time.time()
    print("Start Time:", datetime.now().strftime("%H:%M:%S.%f - %g/%m/%Y"))
    s.run()

    wait(futures)
    run_duration_sec = time.time() - start_time
    avg_latency = 1.0*sum(local_latency_stats)/len(local_latency_stats)

    print("###############################################")
    print("###########   Stop Forrest Stop!!   ###########")
    print("###############################################")
    
    print("Run Duration (sec): %.6f" % run_duration_sec, "Total Requests: %d - Error Request: %d - Timing Error Requests: %d - Average Latency (ms): %.6f - Request rate (req/sec) %.6f" % (workload_events, error_requests.value, timing_error_requests, avg_latency, 1.0*workload_events/run_duration_sec))

    if run_after_workload is not None:
        args = {"run_duration_sec": run_duration_sec,
                "last_print_time_ms": last_print_time_ms,
                "requests_processed": processed_requests,
                "timing_error_number": timing_error_requests,
                "total_request": workload_events,
                "error_request": error_requests,
                "runner_results_file": f"{output_path}/{result_file}.txt"
                }
        run_after_workload(args)

def periodic_runner():
    global start_time, stats, local_latency_stats, runner_parameters

    if 'rate' in runner_parameters.keys():
        rate=runner_parameters['rate']
    else:
        rate = 1
    
    if 'ingress_service' in runner_parameters.keys():
        srv=runner_parameters['ingress_service']
    else:
        srv = 's0'
    
    stats = list()
    print("###############################################")
    print("############   Run Forrest Run!!   ############")
    print("###############################################")
    
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(threads)
    futures = list()
    event={'service':srv,'time':0}
    offset=10 # initial delay to allow the insertion of events in the event list
    for i in range(workload_events):
        event_time =  offset + i * 1.0/rate
        s.enter(event_time, 1, job_assignment, argument=(pool, futures, event, stats, local_latency_stats))

    start_time = time.time()
    print("Start Time:", datetime.now().strftime("%H:%M:%S.%f - %g/%m/%Y"))
    s.run()

    wait(futures)
    run_duration_sec = time.time() - start_time
    avg_latency = 1.0*sum(local_latency_stats)/len(local_latency_stats)

    print("###############################################")
    print("###########   Stop Forrest Stop!!   ###########")
    print("###############################################")
    
    print("Run Duration (sec): %.6f" % run_duration_sec, "Total Requests: %d - Error Request: %d - Timing Error Requests: %d - Average Latency (ms): %.6f - Request rate (req/sec) %.6f" % (workload_events, error_requests.value, timing_error_requests, avg_latency, workload_events/run_duration_sec))

    if run_after_workload is not None:
        args = {"run_duration_sec": run_duration_sec,
                "last_print_time_ms": last_print_time_ms,
                "requests_processed": processed_requests,
                "timing_error_number": timing_error_requests,
                "total_request": workload_events,
                "error_request": error_requests,
                "runner_results_file": f"{output_path}/{result_file}.txt"
                }
        run_after_workload(args)
 

### Main

RUNNER_PATH = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The Runner Parameters file', default=f'{RUNNER_PATH}/RunnerParameters.json')

argcomplete.autocomplete(parser)

try:
    args = parser.parse_args()
except ImportError:
    print("Import error, there are missing dependencies to install.  'apt-get install python3-argcomplete "
          "&& activate-global-python-argcomplete3' may solve")
except AttributeError:
    parser.print_help()
except Exception as err:
    print("Error:", err)

parameters_file_path = args.parameters_file

last_print_time_ms = 0
run_after_workload = None
timing_error_requests = 0
processed_requests = Counter()
error_requests = Counter()
pending_requests = Counter()



try:
    with open(parameters_file_path) as f:
        params = json.load(f)
    runner_parameters = params['RunnerParameters']
    runner_type = runner_parameters['workload_type'] # {workload (default), greedy}
    workload_events = runner_parameters['workload_events'] # n. request for greedy
    ms_access_gateway = runner_parameters["ms_access_gateway"] # nginx access gateway ip
    workloads = runner_parameters["workload_files_path_list"] 
    threads = runner_parameters["thread_pool_size"] # n. parallel threads
    round = runner_parameters["workload_rounds"]  # number of repetition rounds
    result_file = runner_parameters["result_file"]  # number of repetition rounds
    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = RUNNER_PATH
    if "AfterWorkloadFunction" in params.keys() and len(params["AfterWorkloadFunction"]) > 0:
        sys.path.append(params["AfterWorkloadFunction"]["file_path"])
        run_after_workload = getattr(importlib.import_module(params["AfterWorkloadFunction"]["file_path"].split("/")[-1]),
                                     params["AfterWorkloadFunction"]["function_name"])

except Exception as err:
    print("ERROR: in Runner Parameters,", err)
    exit(1)


## Check if "workloads" is a directory path, if so take all the workload files inside it
if os.path.isdir(workloads[0]):
    dir_workloads = workloads[0]
    workloads = list()
    src_files = os.listdir(dir_workloads)
    for file_name in src_files:
        full_file_name = os.path.join(dir_workloads, file_name)
        if os.path.isfile(full_file_name):
            workloads.append(full_file_name)


stats = list()
local_latency_stats = list()
start_time = 0.0

if runner_type=="greedy":
    greedy_runner()
    with open(f"{output_path}/{result_file}.txt", "w") as f:
        f.writelines("\n".join(stats))

elif runner_type=="periodic": 
    periodic_runner()
    with open(f"{output_path}/{result_file}.txt", "w") as f:
        f.writelines("\n".join(stats))
else:
    # default runner is "file" type
    for cnt, workload_var in enumerate(workloads):
        for x in range(round):
            print("Round: %d -- workload: %s" % (x+1, workload_var))
            processed_requests.value = 0
            timing_error_requests = 0
            error_requests.value = 0
            file_runner(workload_var)
            print("***************************************")
        if cnt != len(workloads) - 1:
            print("Sleep for 100 sec to allow completion of previus requests")
            time.sleep(100)
        with open(f"{output_path}/{result_file}_{workload_var.split('/')[-1].split('.')[0]}.txt", "w") as f:
            f.writelines("\n".join(stats))
 
