import random
import os

WORKMODEL_PATH = os.path.dirname(os.path.abspath(__file__))


# Select exactly one service function according to the probability
# Get in INPUT the list with the internal-service functions
def select_internal_service(internal_services):
    internal_service_items = internal_services.items()
    random_extraction = random.random()
    # print("Extraction: %.4f" % random_extraction)
    p_total = 0.0
    for v in internal_services.values():
        p_total += v["probability"]
    p_total = round(p_total, 10)
    prev_interval = 0
    for k in internal_services.keys():
        if random_extraction <= prev_interval + internal_services[k]["probability"]/p_total:
            function_id = k       
            return function_id
        prev_interval += round(internal_services[k]["probability"]/p_total, 10)


def get_work_model(service_graph, workmodel_params):
    work_model = dict()
    
    if "override" in workmodel_params.keys():
        override = workmodel_params["override"]["value"]
    else:
        override = dict()
    
    # Check if the global request_protocol is present, if yes it's override all the functions request_protocol
    exist_global_request_protocol = False
    if "request_protocol" in workmodel_params.keys():
        request_protocol = workmodel_params["request_protocol"]["value"]
        exist_global_request_protocol = True
        # print(f"Request Protocol: {request_protocol}")
        request_method = workmodel_params["request_protocol"].get("method", "get").lower()
        # print(f"Request Method: {request_method}")
        
        request_parameters = workmodel_params["request_protocol"].get("parameters", None)
        if request_method == "post" and not request_parameters:
            raise Exception("ERROR: 'parameters' not found in  'request_protocol' in workModelParameters")        

    # print(f"exist_global_request_protocol: {exist_global_request_protocol}")
    
    databases_prefix = workmodel_params["databases_prefix"]["value"]

    internal_services = dict()
    internal_services_db = dict()

    for k in workmodel_params.keys():
        w=workmodel_params[k]
        if w["type"]!="function":
            continue

        tmp_dict = dict() # string to be inserted as internal service in workmodel.json if this function is chosen
        if not exist_global_request_protocol:
            print("No global request protocol")
            if "request_protocol" in w["value"]:
                request_protocol = w["value"]["request_protocol"]
                    
                request_method = w["value"].get("request_method", "get").lower()
                # TODO is request_parameters mandatory? if yes add a check
                request_parameters = w["value"].get("request_parameters", None)
                print("--------- request_parameters: ", request_parameters)
                if request_method == "post":
                    if not request_parameters:
                        raise Exception("ERROR: request_parameters not found in workModelParameters")
            else:
                request_protocol = "http"
                request_method = "get"

        
        tmp_dict.update({"internal_service": {w["value"]["name"]: w["value"]["parameters"]}})
        tmp_dict.update({"request_protocol": request_protocol})
        if request_protocol == "http":
            tmp_dict.update({"request_method": request_method})
            
            if request_method == "post":
                tmp_dict.update({"request_parameters": request_parameters})


        # print(f"tmp_dict------- {tmp_dict} ************\n")
        if "workers" in w["value"]:
            tmp_dict.update({"workers": w["value"]["workers"]})
        if "threads" in w["value"]:
            tmp_dict.update({"threads": w["value"]["threads"]})
        if "replicas" in w["value"]:
            tmp_dict.update({"replicas": w["value"]["replicas"]})
        if "cpu-limits" in w["value"]:
            tmp_dict.update({"cpu-limits": w["value"]["cpu-limits"]})
        if "cpu-requests" in w["value"]:
            tmp_dict.update({"cpu-requests": w["value"]["cpu-requests"]})
        if "memory-limits" in w["value"]:
            tmp_dict.update({"memory-limits": w["value"]["memory-limits"]})
        if "memory-requests" in w["value"]:
            tmp_dict.update({"memory-requests": w["value"]["memory-requests"]})
        if "recipient" in w["value"] and w["value"]["recipient"] == "database":
            internal_services_db[k]=dict()
            internal_services_db[k].update({"string" : tmp_dict})
            internal_services_db[k].update({"probability": w["value"]["probability"]})
        elif "recipient" in w["value"] and w["value"]["recipient"] == "service":
            internal_services[k]=dict()
            internal_services[k].update({"string" : tmp_dict})
            internal_services[k].update({"probability": w["value"]["probability"]})
    
    if len(internal_services_db) == 0:
        # in case internal services for databases wer not specified, those for plain service are used
        internal_services_db = internal_services
    try:
        for vertex in service_graph.keys():
            work_model[f"{vertex}"] = {'external_services':service_graph.get(vertex)['external_services']}
            
            if vertex.startswith(databases_prefix):
                selected_internal_service = select_internal_service(internal_services_db)
                work_model[f"{vertex}"].update(internal_services_db[selected_internal_service]['string'])
            else:
                selected_internal_service = select_internal_service(internal_services)
                work_model[f"{vertex}"].update(internal_services[selected_internal_service]['string'])
            
            if vertex in override.keys():
                if "sidecar" in override[vertex].keys():
                    work_model[f"{vertex}"].update({"sidecar": override[vertex]["sidecar"]})
                if "function_id" in override[vertex].keys():
                    work_model[f"{vertex}"].update(internal_services[override[vertex]['function_id']]['string'])

    except Exception as err:
        print("ERROR: in get_work_model,", err)
        exit(1)
    
    print("Work Model Created!")
    return work_model
