from WorkLoadGenerator import get_workload, json, pprint


# INPUT params:
# ingress_list = {"s1": 1, "s2": 0.8, "s4": 0.5}
ingress_service = "s0"
mean_interarrival_time = 50
stop_event = 5
request_parameters = {"stop_event": stop_event, "mean_interarrival_time": mean_interarrival_time}
####################


# workload = get_workload(ingress_list, {"min": 1, "max": 3}, request_parameters)
workload = get_workload(ingress_service, request_parameters)
pprint(workload)
print("# Events: %d" % len(workload))
keyboard_input = input("Save work model on file? (y)") or "y"

if keyboard_input == "y":
    # with open(f"workload_events_{stop_event}_mean_{mean_interarrival_time}.json", "w") as f:
    with open(f"workload_test{mean_interarrival_time}.json", "w") as f:
        f.write(json.dumps(workload))


