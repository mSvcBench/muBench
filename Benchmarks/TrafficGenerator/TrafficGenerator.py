import random
import os

Traffic_PATH = os.path.dirname(os.path.abspath(__file__))

def get_Traffic(Traffic_params):
    ingress_service = Traffic_params["ingress_service"]
    request_params = Traffic_params["request_parameters"]
    Traffic_l = list()
    events_cnt = 0
    time = 0

    while events_cnt < request_params["stop_event"]:
        Traffic_l.append({"time": time, "service": ingress_service})
        next_event = round(random.expovariate(1 / request_params["mean_interarrival_time"]))  # Gli interarrivi sono exp neg, il tempo in millisecondi
        time += next_event
        events_cnt += 1

    return Traffic_l

