import random
import os

WORKMODEL_PATH = os.path.dirname(__file__)


# Select exactly one service function according to the probability
# Get in INPUT the list with the internal-service functions
def select_internal_service(internal_services):
    internal_service_items = internal_services.items()
    random_extraction = random.random()
    # print("Extraction: %.4f" % random_extraction)
    p_total = 0.0
    for internal_service in internal_services.values():
        p_total += internal_service["probability"]
    p_total = round(p_total, 10)
    prev_interval = 0
    for internal_service in internal_service_items:
        if random_extraction <= prev_interval + internal_service[1]["probability"]/p_total:
            tmp_param = dict(internal_service[1])
            tmp_param.pop("probability")
            return {internal_service[0]: tmp_param}
        prev_interval += round(internal_service[1]["probability"]/p_total, 10)


def get_work_model(service_mesh, workmodel_params):
    work_model = dict()
    request_method = workmodel_params["request_method"]
    workmodel_params.pop('request_method', None)
    databases_prefix = workmodel_params["databases_prefix"]
    workmodel_params.pop('databases_prefix', None)
    # pprint(params)

    internal_services = dict()
    internal_services_db = dict()

    for x in workmodel_params.items():

        if "type" in dict(x[1]) and dict(x[1])["type"] == "database":
            x[1].pop("type")
            internal_services_db[x[0]] = x[1]
        else:
            internal_services[x[0]] = x[1]

    if len(internal_services_db) == 0:
        internal_services_db = internal_services
    try:
        for vertex in service_mesh.keys():
            if vertex.startswith(databases_prefix):
                internal_service_pool = internal_services_db
            else:
                internal_service_pool = internal_services

            work_model[f"{vertex}"] = {"internal_service": select_internal_service(internal_service_pool),
                                       "request_method": request_method},
    except Exception as err:
        print("ERROR: in creation work model,", err)
        exit(1)

    # pprint(work_model)
    print("Work Model Created!")
    return work_model
