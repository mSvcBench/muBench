import json
import os
from pprint import pprint


# Variabili di test
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


#########

YAML_OUTPUT_FILE = "MicroServiceDeployment"
NAMESPACE = "default"
IMAGE = "lucapetrucci/microservice:latest"
CLUSTER_DOMAIN = "cluster"
PATH = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}


# Add params to work_model json
# http://s1.default.svc.cluster.local
def add_param_to_work_model(model, path, name_space, cluster_domain, image):
    for service in model:
        model[service].update({"url": f"http://{service}.{name_space}.svc.{cluster_domain}.local"})
        model[service].update({"path": path})
        model[service].update({"image": image})
        model[service].update({"namespace": name_space})
    print("Work Model Updated!")


def create_deployment_yaml_files(model, args):
    for service in model:
        with open('DeploymentTemplate.yaml', 'r') as file:
            f = file.read()
            f = f.replace("{{SERVICE_NAME}}", service)
            f = f.replace("{{IMAGE}}", model[service]["image"])
            f = f.replace("{{NAMESPACE}}", model[service]["namespace"])
            for key in args:
                f = f.replace(key, args[key])

        if not os.path.exists("yamls"):
            os.makedirs("yamls")

        with open(f"yamls/{YAML_OUTPUT_FILE}-{service}.yaml", 'w') as file:
            file.write(f)
    print("Deployment Created!")


def create_configmap_yaml(mesh, model, namespace):
    with open('ConfigMapTemplate.yaml', 'r') as file:
        f = file.read()
        f = f.replace("{{SERVICE_MESH}}", json.dumps(mesh))
        f = f.replace("{{WORK_MODEL}}", json.dumps(model))
        f = f.replace("{{NAMESPACE}}", namespace)

    if not os.path.exists("yamls"):
        os.makedirs("yamls")

    with open("yamls/ConfigMapMicroService.yaml", 'w') as file:
        file.write(f)

    print("ConfigMap Created!")


add_param_to_work_model(work_model, PATH, NAMESPACE, CLUSTER_DOMAIN, IMAGE)
# pprint(work_model)

create_deployment_yaml_files(work_model, var_to_be_replaced)

# create_configmap_yaml(service_mesh, work_model, NAMESPACE)

