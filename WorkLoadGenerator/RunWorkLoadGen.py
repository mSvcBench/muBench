from WorkLoadGenerator import get_workload, WORKLOAD_PATH
import json
from pprint import pprint

try:
    with open(f'{WORKLOAD_PATH}/WorkLoadParameters.json') as f:
        params = json.load(f)
    workload_parameters = params['WorkLoadParameters']

    ingress_service = workload_parameters['ingress_service']
    request_parameters = workload_parameters['request_parameters']
except Exception as err:
    print("ERROR: in RunWorkLoadGen,", err)
    exit(1)


# workload = get_workload(ingress_list, {"min": 1, "max": 3}, request_parameters)
workload = get_workload(ingress_service, request_parameters)
pprint(workload)
print("# Events: %d" % len(workload))
# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    # with open(f"workload_events_{stop_event}_mean_{mean_interarrival_time}.json", "w") as f:
    with open(f"{WORKLOAD_PATH}/workload_test{request_parameters['mean_interarrival_time']}.json", "w") as f:
        f.write(json.dumps(workload))

    print(f"'{WORKLOAD_PATH}/workload_test{request_parameters['mean_interarrival_time']}.json'")
    print("File Saved!")


