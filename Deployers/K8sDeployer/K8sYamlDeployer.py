from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import yaml
import json
import os
import time


def deploy_items(folder,st):
    print("######################")
    print(f"We are going to DEPLOY the yaml files in the following folder: {folder}")
    print("######################")
    config.load_kube_config()
    k8s_apps_api = client.AppsV1Api()
    k8s_core_api = client.CoreV1Api()
    items = list()
    for r, d, f in os.walk(folder):
        f.sort(reverse=True)    # userd to deploy first pods demanding more resources
        for file in f:
            if '.yaml' in file:
                items.append(os.path.join(r, file))

    if os.path.isfile(folder):
        items.append(folder)

    for yaml_to_apply in items:
        with open(yaml_to_apply) as f:
            complete_yaml = yaml.load_all(f,Loader=yaml.FullLoader)
            for partial_yaml in complete_yaml:
                try:
                    if partial_yaml["kind"] == "Deployment":
                        k8s_apps_api.create_namespaced_deployment(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                        dn=partial_yaml['metadata']['name']
                        api_response = k8s_apps_api.read_namespaced_deployment_status(name=partial_yaml['metadata']['name'], namespace=partial_yaml["metadata"]["namespace"], pretty=True)
                        while (api_response.status.ready_replicas != api_response.status.replicas):
                            print(f"\n *** Waiting deployment {dn} ready ...*** \n")
                            time.sleep(1)
                            api_response = k8s_apps_api.read_namespaced_deployment_status(name=partial_yaml['metadata']['name'], namespace=partial_yaml["metadata"]["namespace"], pretty=True)
                        time.sleep(st) # used to avoid API server overload
                        print(f"Deployment {dn} created.")
                    elif partial_yaml["kind"] == "Service":
                        k8s_core_api.create_namespaced_service(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                        print(f"Service '{partial_yaml['metadata']['name']}' created.")
                        print("---")
                    elif partial_yaml["kind"] == "ConfigMap":
                            k8s_core_api.create_namespaced_config_map(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                            print(f"ConfigMap '{partial_yaml['metadata']['name']}' created.")
                            print("---")
                except ApiException as err:
                    api_exception_body = json.loads(err.body)
                    print("######################")
                    print(f"Exception raised deploying a {partial_yaml['kind']}: {api_exception_body['details']} -> {api_exception_body['reason']}")
                    print("######################")                

def undeploy_items(folder):
    print("######################")
    print(f"We are going to UNDEPLOY the yaml files in the following folder: {folder}")
    print("######################")
    config.load_kube_config()
    k8s_apps_api = client.AppsV1Api()
    k8s_core_api = client.CoreV1Api()
    items = list()
    for r, d, f in os.walk(folder):
        for file in f:
            if '.yaml' in file:
                items.append(os.path.join(r, file))
    if os.path.isfile(folder):
        items.append(folder)
    for yaml_to_create in items:
        with open(yaml_to_create) as f:
            complete_yaml = yaml.load_all(f,Loader=yaml.FullLoader)
            for partial_yaml in complete_yaml:
                try:
                    if partial_yaml["kind"] == "Deployment":
                        dep_name = partial_yaml["metadata"]["name"]
                        resp = k8s_apps_api.delete_namespaced_deployment(name=dep_name, namespace=partial_yaml["metadata"]["namespace"], grace_period_seconds=0)
                        print(f"Deployment '{dep_name}' deleted.")
                    elif partial_yaml["kind"] == "Service":
                        svc_name = partial_yaml["metadata"]["name"]
                        resp = k8s_core_api.delete_namespaced_service(name=svc_name, namespace=partial_yaml["metadata"]["namespace"], grace_period_seconds=0)
                        print(f"Service '{svc_name}' deleted.")
                        print("---")
                    elif partial_yaml["kind"] == "ConfigMap":
                        map_name = partial_yaml["metadata"]["name"]
                        resp = k8s_core_api.delete_namespaced_config_map(name=map_name, namespace=partial_yaml["metadata"]["namespace"])
                        print(f"ConfigMap '{map_name}' deleted.")
                        print("---")
                except ApiException as err:
                    api_exception_body = json.loads(err.body)
                    print("######################")
                    print(f"Exception raised trying to delete {partial_yaml['kind']} '{api_exception_body['details']['name']}': {api_exception_body['reason']}")
                    print("######################")
