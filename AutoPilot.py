from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import json

import ServiceMeshGenerator.ServiceMeshGenerator as smGen
import WorkModelGenerator.WorkModelGenerator as wmGen
import WorkLoadGenerator.WorkLoadGenerator as wlGen
import K8sYamlBuilder.K8sYamlBuilder as K8sBuilder
import K8sDeployer.K8sDeployer as K8sDeployer
import yaml
import os

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
mean_interarrival_time = 100  # Mean of request interarrival

#### K8s Yaml Builder

yaml_output_file_name = "MicroServiceDeployment"
deployment_namespace = "default"
image_name = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
service_path = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

###########################
##          RUN          ##
###########################
# TODO chiedere del workload all'utente
# min_max = {"min": min_services, "max": max_services}
# request_parameters = {"stop_event": 10, "mean_interarrival": 100}
# workload = wlGen.get_workload(ingress_dict, min_max, request_parameters)

folder_not_exist = False
if os.path.exists(f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"):
    folder = f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"
else:
    folder_not_exist = True



def create_deployment_config():
    print("---")
    service_mesh_params = {"services_groups": services_groups,
                           "vertices": vertices,
                           "power": power,
                           "edges_per_vertex": edges_per_vertex,
                           "zero_appeal": zero_appeal
                           }
    servicemesh = smGen.get_service_mesh(service_mesh_params)

    workmodel = wmGen.get_work_model(vertices, work_model_params)

    K8sBuilder.customization_work_model(workmodel, service_path, deployment_namespace, cluster_domain, image_name)
    # pprint(workmodel)

    K8sBuilder.create_deployment_yaml_files(workmodel, var_to_be_replaced)
    created_items = os.listdir(f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls")
    print(f"The following files are created: {created_items}")
    print("---")
    # return a list of the files just created
    return created_items, servicemesh, workmodel


def remove_files(folder_v):
    try:

        folder_items = os.listdir(folder_v)
        for item in folder_items:
            os.remove(f"{folder_v}/{item}")

        print("######################")
        print(f"Following files removed: {folder_items}")
        print("######################")
    except Exception as er:
        print("######################")
        print(f"Error removing following files: {er}")
        print("######################")


######## SCRIPT
try:
    if folder_not_exist or len(os.listdir(folder)) == 0:
        keyboard_input = input("\nDirectory empty, wanna DEPLOY?")
        if keyboard_input == "":
            updated_folder_items, service_mesh, work_model = create_deployment_config()
            # deploy_items(updated_folder_items)
            K8sDeployer.deploy_items(folder)
        else:
            print("...\nOk you do not want to DEPLOY stuff! Bye!")
    else:
        print("######################")
        print("!!!! Warning !!!!")
        print("######################")
        print(f"Folder is not empty: {folder}.")
        keyboard_input = input("Wanna UNDEPLOY old yamls first, delete the files and then start again?")
        if keyboard_input == "":
            # undeploy_items(folder_items)
            K8sDeployer.undeploy_items(folder)
            remove_files(folder)
            # updated_folder_items = create_deployment_config()
            # deploy_items(updated_folder_items)
        else:
            print("...\nOk you want to keep the OLD deployment! Bye!")

except Exception as err:
    print("######################")
    print(f"Exception in 'main': {err}")
    print("######################")
except KeyboardInterrupt:
    print("\n...\nBye bye!")

