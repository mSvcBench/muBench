import ServiceMeshGenerator.ServiceMeshGenerator as smGen
import WorkModelGenerator.WorkModelGenerator as wmGen
import WorkLoadGenerator.WorkLoadGenerator as wlGen
import K8sYamlBuilder.K8sYamlBuilder as K8sBld


from pprint import pprint

############### Input Param ###############
vertices = 5

##### ServiceMesh Params
services_groups = 1  # Number of services for group
power = 1  # Power ???
edges_per_vertex = 1  # ??
zero_appeal = 10  # ??


##### WorkModel Params
# Possible Internal Job Functions with params
work_model_params = {"compute_pi": {"P": 1, "b": 11, "c": [101, 101]},
                     "ave_luca": {"P": 0.6, "ave_number": 13, "b": 42}
                     }

##### Workload
ingress_dict = {"s1": 1, "s2": 0.8, "s4": 0.5}  # Dictionary of possibile ingress Services with associated probability
min_services = 1  # MIN number of selected ingress dictionary
max_services = 1  # MAX number of selected ingress dictionary

event_number = 10  # Number of event until the end of simulation
request_time_interval_s = 3  # Time in seconds until the end of simulation
interarrival_mean = 100  # Mean of request interarrival



# RUN

service_mesh_params = {"services_groups": services_groups,
                       "vertices": vertices,
                       "power": power,
                       "edges_per_vertex": edges_per_vertex,
                       "zero_appeal": zero_appeal
                       }
service_mesh = smGen.get_service_mesh(service_mesh_params)


work_model = wmGen.get_work_model(vertices, work_model_params)


min_max = {"min": min_services, "max": max_services}
request_parameters = {"event_number": 10, "request_time_interval_s": 3, "interarrival_mean": 100}
workload = wlGen.get_workload(ingress_dict, min_max, request_parameters)


YAML_OUTPUT_FILE = "MicroServiceDeployment"
NAMESPACE = "default"
IMAGE = "lucapetrucci/microservice:latest"
CLUSTER_DOMAIN = "cluster"
PATH = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

K8sBld.add_param_to_work_model(work_model, PATH, NAMESPACE, CLUSTER_DOMAIN, IMAGE)
# pprint(work_model)

K8sBld.create_deployment_yaml_files(work_model, var_to_be_replaced)


# asd = input("CIAO")

# print(asd)


# print("Service Mesh")
# pprint(service_mesh)
# print("Workmodel")
# pprint(work_model)
# print("Workload")
# pprint(workload)

