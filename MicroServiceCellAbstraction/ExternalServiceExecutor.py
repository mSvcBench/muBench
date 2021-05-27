import random
import requests
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import time

work_model = dict()


def external_service(group):
    print("**** Start SERVICES nel thread: %s" % str(group))
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
            r = requests.get(f'{work_model[service]["url"]}{work_model[service]["path"]}')
            print("Service: %s -> Status_code: %s -- len(text): %d" % (service, r.status_code, len(r.text)))
        except Exception as err:
            service_error_dict[service] = err
            service_error_flag = True
            print("Error in request external service %s -- %s" % (service, str(err)))

    print("#### SERVICE Done!")
    return service_error_flag, service_error_dict


def run_external_service_REST(jobs_group, model):
    print("** EXTERNAL SERVICES")
    global work_model
    work_model = model

    number_of_groups = len(jobs_group)
    pool = ThreadPoolExecutor(number_of_groups)

    futures = list()

    for group in jobs_group:
        futures.append(pool.submit(external_service, group))

    wait(futures)

    service_error_dict = dict()
    for x in as_completed(futures):
        if x.result()[0]:
            service_error_dict.update(x.result()[1])

    wait(futures)
    print("--------> Threads Done!")
    return service_error_dict

