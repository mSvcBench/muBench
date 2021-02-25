import yaml
import os
from K8sYamlBuilder import *
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

WORKING_PATH = os.path.dirname(__file__) or '.'

######### Variabili di test #########

service_mesh = {"s0": [{"seq_len": 1,
                        "services": ["s2", "s3"]
                        },
                       {"seq_len": 1,
                        "services": ["s3"]
                        }
                       ],
                "s1": [],
                "s2": [{"seq_len": 1,
                        "services": ["s4"]}],
                "s3": [],
                "s4": []
                }

work_model = {'s0': {'params': {'ave_luca': {'P': 0.6, 'ave_number': 13, 'b': 42}}},
              's1': {'params': {'compute_pi': {'P': 1, 'b': 11, 'c': [101, 101]}}},
              's2': {'params': {'compute_pi': {'P': 1, 'b': 11, 'c': [101, 101]}}},
              's3': {'params': {'compute_pi': {'P': 1, 'b': 11, 'c': [101, 101]}}},
              's4': {'params': {'compute_pi': {'P': 1, 'b': 11, 'c': [101, 101]}}}}


YAML_OUTPUT_FILE = "MicroServiceDeployment"
NAMESPACE = "default"
IMAGE = "lucapetrucci/microservice:latest"
CLUSTER_DOMAIN = "cluster"
PATH = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

######### Variabili di test #########


def remove_files(folder_items):
    try:
        for item in folder_items:
            os.remove(f"{WORKING_PATH}/yamls/{item}")

        print("######################")
        print(f"Following files removed: {folder_items}")
        print("######################")
    except Exception as err:
        print("######################")
        print(f"Error removing following files: {err}")
        print("######################")


def deploy_items(items):
    print("######################")
    print(f"We are going to DEPLOY the following items: {items}")
    print("######################")

    config.load_kube_config()
    k8s_apps_api = client.AppsV1Api()
    k8s_core_api = client.CoreV1Api()

    for yaml_to_create in items:
        print(yaml_to_create)
        with open(f"{WORKING_PATH}/yamls/{yaml_to_create}") as f:

            complete_yaml = yaml.load_all(f)
            for partial_yaml in complete_yaml:
                try:
                    if partial_yaml["kind"] == "Deployment":
                        k8s_apps_api.create_namespaced_deployment(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                        print(f"Deployment '{partial_yaml['metadata']['name']}' created.")
                    elif partial_yaml["kind"] == "Service":
                        k8s_core_api.create_namespaced_service(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                        print(f"Service '{partial_yaml['metadata']['name']}' created.")
                        print("---")
                except ApiException as err:
                    api_exception_body = json.loads(err.body)
                    print("######################")
                    print(f"Exception raised deploying a {partial_yaml['kind']}: {api_exception_body['details']} -> {api_exception_body['reason']}")
                    print("######################")


def undeploy_items(items):
    print("######################")
    print(f"We are going to UNDEPLOY the following items: {items}")
    print("######################")

    config.load_kube_config()
    k8s_apps_api = client.AppsV1Api()
    # k8s_apps_api = client.ExtensionsV1beta1Api()
    k8s_core_api = client.CoreV1Api()

    for yaml_to_create in items:
        with open(f"{WORKING_PATH}/yamls/{yaml_to_create}") as f:

            complete_yaml = yaml.load_all(f)
            for partial_yaml in complete_yaml:
                try:
                    if partial_yaml["kind"] == "Deployment":
                        dep_name = partial_yaml["metadata"]["name"]
                        resp = k8s_apps_api.delete_namespaced_deployment(name=dep_name, namespace=partial_yaml["metadata"]["namespace"])
                        print(f"Deployment '{dep_name}' deleted. Status={resp.status}")
                    elif partial_yaml["kind"] == "Service":
                        svc_name = partial_yaml["metadata"]["name"]
                        resp = k8s_core_api.delete_namespaced_service(name=svc_name, namespace=partial_yaml["metadata"]["namespace"])
                        print(f"Service '{svc_name}' deleted. Status={resp.status}")
                        print("---")
                except ApiException as err:
                    api_exception_body = json.loads(err.body)
                    print("######################")
                    print(f"Exception raised trying to delete {partial_yaml['kind']} '{api_exception_body['details']['name']}': {api_exception_body['reason']}")
                    print("######################")


def create_deployment_config():
    print("---")
    add_param_to_work_model(work_model, PATH, NAMESPACE, CLUSTER_DOMAIN, IMAGE)
    create_deployment_yaml_files(work_model, var_to_be_replaced)
    created_items = os.listdir(f"{WORKING_PATH}/yamls")
    print(f"The following files are created: {created_items}")
    print("---")
    # return a list of the files just created
    return created_items


def main():
    folder_items = os.listdir(f"{WORKING_PATH}/yamls")

    try:
        if len(folder_items) == 0:
            keyboard_input = input("\nDirectory empty, wanna DEPLOY?")
            if keyboard_input == "":
                updated_folder_items = create_deployment_config()
                deploy_items(updated_folder_items)
            else:
                print("...\nOk you do not want to DEPLOY stuff! Bye!")
        else:
            print("######################")
            print("!!!! Warning !!!!")
            print("######################")
            print(f"Folder is not empty: {folder_items}.")
            keyboard_input = input("Wanna UNDEPLOY old yamls first, delete the files and then start again?")
            if keyboard_input == "":
                undeploy_items(folder_items)
                remove_files(folder_items)
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

main()