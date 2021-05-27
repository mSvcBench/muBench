import json
import os
from pprint import pprint

K8s_YAML_BUILDER_PATH = os.path.dirname(__file__)

# Variabili di test

# work_model = {'s0': {'params': {'ave_luca': {'ave_number': 13, 'mean_bandwidth': 42}}},
#               's1': {'params': {'compute_pi': {'mean_bandwidth': 11, 'range_complexity': [101, 101]}}},
#               's2': {'params': {'compute_pi': {'mean_bandwidth': 11, 'range_complexity': [101, 101]}}},
#               's3': {'params': {'compute_pi': {'mean_bandwidth': 11, 'range_complexity': [101, 101]}}},
#               's4': {'params': {'compute_pi': {'mean_bandwidth': 11, 'range_complexity': [101, 101]}}}}


# PREFIX_YAML_FILE = "MicroServiceDeployment"
# NAMESPACE = "default"
# IMAGE = "lucapetrucci/microservice:latest"
# CLUSTER_DOMAIN = "cluster"
# PATH = "/api/v1"
# # var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
# var_to_be_replaced = {}


# Add params to work_model json
# http://s1.default.svc.cluster.local
def customization_work_model(model, k8s_parameters):
    for service in model:
        model[service].update({"url": f"http://{service}.{k8s_parameters['namespace']}.svc.{k8s_parameters['cluster_domain']}.local"})
        model[service].update({"path": k8s_parameters['path']})
        model[service].update({"image": k8s_parameters['image']})
        model[service].update({"namespace": k8s_parameters['namespace']})
    print("Work Model Updated!")


def create_deployment_yaml_files(model, k8s_parameters, nfs):
    namespace = k8s_parameters['namespace']
    for service in model:
        with open(f"{K8s_YAML_BUILDER_PATH}/Template/DeploymentTemplate.yaml", "r") as file:
            f = file.read()
            f = f.replace("{{SERVICE_NAME}}", service)
            f = f.replace("{{IMAGE}}", model[service]["image"])
            f = f.replace("{{NAMESPACE}}", namespace)
            # for key in args:
            #     f = f.replace(key, args[key])

        if not os.path.exists(f"{K8s_YAML_BUILDER_PATH}/yamls"):
            os.makedirs(f"{K8s_YAML_BUILDER_PATH}/yamls")

        with open(f"{K8s_YAML_BUILDER_PATH}/yamls/{k8s_parameters['prefix_yaml_file']}-{service}.yaml", "w") as file:
            file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Template/ConfigMapNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)

    with open(f"{K8s_YAML_BUILDER_PATH}/yamls/ConfigMapNginxGw.yaml", "w") as file:
        file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Template/DeploymentNginxGwTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)

    with open(f"{K8s_YAML_BUILDER_PATH}/yamls/DeploymentNginxGw.yaml", "w") as file:
        file.write(f)

    with open(f"{K8s_YAML_BUILDER_PATH}/Template/PersistentVolumeMicroServiceTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{NAMESPACE}}", namespace)
        f = f.replace("{{SERVER}}", nfs["address"])
        f = f.replace("{{PATH}}", nfs["mount_path"])

    with open(f"{K8s_YAML_BUILDER_PATH}/yamls/PersistentVolumeMicroService.yaml", "w") as file:
        file.write(f)

    print("Deployment Created!")



def create_configmap_yaml(mesh, model, namespace):
    with open(f"{K8s_YAML_BUILDER_PATH}/Template/ConfigMapTemplate.yaml", "r") as file:
        f = file.read()
        f = f.replace("{{SERVICE_MESH}}", json.dumps(mesh))
        f = f.replace("{{WORK_MODEL}}", json.dumps(model))
        f = f.replace("{{NAMESPACE}}", namespace)

    if not os.path.exists("yamls"):
        os.makedirs("yamls")

    with open(f"{K8s_YAML_BUILDER_PATH}/yamls/ConfigMapMicroService.yaml", "w") as file:
        file.write(f)

    print("ConfigMap Created!")

#
# customization_work_model(work_model, PATH, NAMESPACE, CLUSTER_DOMAIN, IMAGE)
# pprint(work_model)

# create_deployment_yaml_files(work_model, PREFIX_YAML_FILE, var_to_be_replaced)

