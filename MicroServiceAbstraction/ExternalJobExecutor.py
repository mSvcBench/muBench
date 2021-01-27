import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED


def external_job(group):
    print("**** RUN_JOB")
    print("**** Group of Jobs nel thread %s" % str(group))
    # Randomly select seq_len elements from services in the group
    selected_services = random.sample(group["services"], k=group["seq_len"])
    for service in selected_services:
        sleep_time = random.randint(2, 5)
        print("******** Service:%s -- Sleep for %d" % (service, sleep_time))
        time.sleep(sleep_time)
        r = requests.get('http://localhost:8888/%s' % service)
        print("Status_code: %s -- text: %s" % (r.status_code, r.text))

    print("**** JOB Done!")


def run_external_jobs_REST(jobs_group):
    print("** EXTERNAL JOBS")
    number_of_groups = len(jobs_group)
    pool = ThreadPoolExecutor(number_of_groups)
    futures = list()

    for group in jobs_group:
        futures.append(pool.submit(external_job, group))

    wait(futures)
    print("--------> Threads Done!")
