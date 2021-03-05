############### Input Params ###############
vertices = 5

##### ServiceMesh Params
services_groups = 1  # Number of services for group
power = 1  # Power ???
edges_per_vertex = 1
zero_appeal = 10


##### WorkModel Params
# Possible Internal Job Functions with params
work_model_params = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [101, 101]},
                     "ave_luca": {"probability": 0.6, "ave_number": 13, "mean_bandwidth": 42}
                     }

##### Workload
ingress_dict = {"s1": 1, "s2": 0.8, "s4": 0.5}  # Dictionary of possibile ingress Services with associated probability
min_services = 1  # MIN number of selected ingress dictionary
max_services = 1  # MAX number of selected ingress dictionary

stop_event = 10  # Number of event until the end of simulation
mean_interarrival_time = 100  # Mean of request interarrival


#### K8s Yaml Builder
prefix_yaml_output_file = "MicroServiceDeployment"
deployment_namespace = "default"
image_name = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
service_path = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}
