import random
import os

WORKLOAD_PATH = os.path.dirname(__file__)

# vertex_number -> N number of vertex
# ingress_services -> {"sx": probability, ...}
# number_of_ingreress -> number of ingress services in range [MIN, MAX]
def get_workload(ingress_service, request_params):
    workload_l = list()
    # print("vertex_number: %d" % vertex_number)
    # print("ingress_services:", ingress_services)
    # print("ingress_number:", ingress_number)
    # print("request_params:", request_params)
    events_cnt = 0
    time = 0

    sim_duration = 180  # Durata della simulazione in secondi
    # while time <= sim_duration*1000:
    while events_cnt < request_params["stop_event"]:
        # selected_ingress_number = random.randint(ingress_number["min"], ingress_number["max"])
        # print("selected_ingress_number:", selected_ingress_number)

        # services = random.sample(list(ingress_services.items()), k=selected_ingress_number)
        selected_services = dict()

        # for service in services:
        #     selected_services[service[0]] = service[1]
        # selected_services[ingress_services[0]] = ingress_services[1]
        workload_l.append({"time": time, "service": ingress_service})

        next_event = round(random.expovariate(1 / request_params["mean_interarrival_time"]))  # Gli interarrivi sono exp neg, il tempo in millisecondi
        time += next_event
        # print("interarrivo", round(next_event, 0))
        events_cnt += 1

    return workload_l

