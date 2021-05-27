############### Input Parameters ###############
##### Service Mesh Parameters
vertices = 10
external_service_groups = 1  # Number of services for group
power = 0.05  # Power ???
edges_per_vertex = 1
zero_appeal = 0.01
# dbs = {}
dbs = {"sdb1": 1, "sdb2": 0.2, "sdb3": 0.1}


##### Work Model Parameters
# Possible Internal Job Functions with params
work_model_params = {"compute_pi": {"probability": 1, "mean_bandwidth": 100, "range_complexity": [300, 300]},
                     # "ave_luca": {"probability": 0.8, "ave_number": 13, "mean_bandwidth": 42}
                     }


##### Workload Parameters
ingress_dict = {"s0": 1}  # Dictionary of possibile ingress Services with associated probability
# ingress_dict = {"s1": 1, "s2": 0.8, "s4": 0.5}  # Dictionary of possibile ingress Services with associated probability
min_services = 1  # MIN number of selected ingress dictionary
max_services = 1  # MAX number of selected ingress dictionary

stop_event = 10  # Number of event until the end of simulation
mean_interarrival_time = 100  # Mean of request interarrival


#### K8s Yaml Builder Parameters
prefix_yaml_output_file = "MicroServiceDeployment"
deployment_namespace = "default"
image_name = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
service_path = "/api/v1"
var_to_be_replaced = {}  # (e.g {"{{string_in_template}}": "new_value", ...} )

nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}


#### Autopilot Parameters
# job_functions_file_path = "AveLuca.py"
job_functions_file_path = ""
