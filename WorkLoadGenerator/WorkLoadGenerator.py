import random
# import numpy as np
import json
from pprint import pprint

# Deve generare in output un file tipo questo
# Workload = [{"time": t0, "services":{"sx": "p", "sx": "p", ...}, ...]
'''
workload = [{"time": 0, "services": {"s1": 1,
                                     "s2": 0.8}
             },
            {"time": 2, "services": {"s1": 1}
             },
            {"time": 5, "services": {"s1": 1,
                                     "s2": 0.8}
             },
            {"time": 7, "services": {"s1": 0.3,
                                     "s4": 0.5}
             },
            {"time": 9, "services": {"s1": 1,
                                     "s2": 0.8}
             },
            {"time": 10, "services": {"s4": 1,
                                      "s7": 0.2}
             },
            {"time": 13, "services": {"s3": 0.3,
                                      "s6": 0.8}
             }
            ]
'''


# vertex_number -> N number of vertex
# ingress_services -> {"sx": probability, ...}
# number_of_ingreress -> number of ingress services in range [MIN, MAX]
def get_workload(ingress_services, ingress_number, request_params):
    workload_l = list()
    # print("vertex_number: %d" % vertex_number)
    # print("ingress_services:", ingress_services)
    # print("ingress_number:", ingress_number)
    # print("request_params:", request_params)

    events_cnt = 0
    time = 0
    while events_cnt < request_params["stop_event"]:

        selected_ingress_number = random.randint(ingress_number["min"], ingress_number["max"])
        # print("selected_ingress_number:", selected_ingress_number)

        services = random.sample(list(ingress_services.items()), k=selected_ingress_number)
        selected_services = dict()

        for service in services:
            selected_services[service[0]] = service[1]
        workload_l.append({"time": time, "services": selected_services})

        next_event = round(random.expovariate(1 / request_params["mean_interarrival_time"]))  # Gli interarrivi sono exp neg, il tempo in millisecondi
        time += next_event
        # print("interarrivo", round(next_event, 0))
        events_cnt += 1

    return workload_l



# Il termine della simulazione e' dato dal numero di eventi, non dal tempo
# ingress_list = {"s1": 1, "s2": 0.8, "s4": 0.5}
# request_parameters = {"stop_event": 10, "mean_interarrival_time": 2}

# workload = get_workload(ingress_list, {"min": 1, "max": 3}, request_parameters)
#
# with open(f"../Runner/workload.json", "w") as f:
#     f.write(json.dumps(workload))
#
# pprint(workload)

