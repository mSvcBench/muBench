import ServiceMeshGenerator.ServiceMeshGenerator as smGen
import WorkModelGenerator.WorkModelGenerator as wmGen
import WorkLoadGenerator.WorkLoadGenerator as wlGen
import K8sYamlBuilder
import K8sYamlBuilder.K8sYamlBuilder as lll


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


print(lll.PATH)

lll.add_param_to_work_model(None,None,None,None,None)
# asd = input("CIAO")

# print(asd)


# print("Service Mesh")
# pprint(service_mesh)
# print("Workmodel")
# pprint(work_model)
# print("Workload")
# pprint(workload)

