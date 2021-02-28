from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import yaml
import json
import os


def deploy_items(folder):
    print("######################")
    print(f"We are going to DEPLOY the yaml files in the following folder: {folder}")
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
            print(yaml_to_create)
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


def deploy_volume(yamls):
    print("######################")
    print(f"We are going to DEPLOY the PersistentVolume Persi and PersistentVolumeClaim from the yaml file: {yamls}")
    print("######################")

    config.load_kube_config()
    k8s_core_api = client.CoreV1Api()

    with open(yamls) as f:
        complete_yaml = yaml.load_all(f)
        for partial_yaml in complete_yaml:
            try:
                if partial_yaml["kind"] == "PersistentVolume":
                    api_response = k8s_core_api.create_persistent_volume(body=partial_yaml)
                    print(f"PersistentVolume '{partial_yaml['metadata']['name']}' created.")
                    print("---")
                elif partial_yaml["kind"] == "PersistentVolumeClaim":
                    api_response = k8s_core_api.create_namespaced_persistent_volume_claim(namespace=partial_yaml["metadata"]["namespace"], body=partial_yaml)
                    print(f"PersistentVolumeClaim '{partial_yaml['metadata']['name']}' created.")
                    print("---")
            except ApiException as err:
                api_exception_body = json.loads(err.body)
                print("######################")
                print(f"Exception raised deploying a {partial_yaml['kind']}: {api_exception_body['details']} -> {api_exception_body['reason']}")
                print("######################")

def undeploy_volume(yamls):
    print("######################")
    print(f"We are going to UNDEPLOY the PersistentVolume Persi and PersistentVolumeClaim from the yaml file: {yamls}")
    print("######################")

    config.load_kube_config()
    k8s_core_api = client.CoreV1Api()

    with open(yamls) as f:
        complete_yaml = yaml.load_all(f)
        for partial_yaml in complete_yaml:
            try:
                if partial_yaml["kind"] == "PersistentVolume":
                    pv_name = partial_yaml["metadata"]["name"]
                    resp = k8s_core_api.delete_persistent_volume(name=pv_name)
                    print(f"Deployment '{pv_name}' deleted. Status={resp.status}")
                elif partial_yaml["kind"] == "PersistentVolumeClaim":
                    pvc_name = partial_yaml["metadata"]["name"]
                    resp = k8s_core_api.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=partial_yaml["metadata"]["namespace"])
                    print(f"Service '{pvc_name}' deleted. Status={resp.status}")
                    print("---")
            except ApiException as err:
                api_exception_body = json.loads(err.body)
                print("######################")
                print(
                    f"Exception raised trying to delete {partial_yaml['kind']} '{api_exception_body['details']['name']}': {api_exception_body['reason']}")
                print("######################")


def deploy_nginx_gateway(nginx_yaml):
    deploy_items(nginx_yaml)

def undeploy_nginx_gateway(nginx_yaml):
    undeploy_items(nginx_yaml)


# deploy_items("../K8sYamlBuilder/yamls")
# undeploy_items("../K8sYamlBuilder/yamls")

# deploy_volume("../../yaml/PersistentVolumeMicroService.yaml")
# undeploy_volume("../../yaml/PersistentVolumeMicroService.yaml")


# deploy_nginx_gateway("../../yaml/DeploymentNginxGw.yaml")
# undeploy_nginx_gateway("../../yaml/DeploymentNginxGw.yaml")
