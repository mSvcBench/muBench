import json
from pprint import pprint

# Variabili di test
service_mesh = {"s1": [{"seq_len": 1,
                        "services": ["s2", "s3"]
                        },
                       {"seq_len": 1,
                        "services": ["s3"]
                        }
                       ],
                "s2": [],
                "s3": [{"seq_len": 1,
                        "services": ["s4"]}],
                "s4": [],
                "s5": []
                }

work_model = {"s1": {"path": "/api/v1",
                     "params": {"c": 101, "b": 11}
                     },
              "s2": {"path": "/api/v1",
                     "params": {"c": 102, "b": 12}
                     },
              "s3": {"path": "/api/v1",
                     "params": {"c": 103, "b": 13}
                     },
              "s4": {"path": "/api/v1",
                     "params": {"c": 104, "b": 14}
                     },
              "s5": {"path": "/api/v1",
                     "params": {"c": 105, "b": 15}
                     }
              }
#########

YAML_OUTPUT_FILE = "MicroServiceDeployment"
NAMESPACE = "default"
IMAGE = "lucapetrucci/microservice:latest"
CLUSTER_DOMAIN = "cluster"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

# Add params to work_model json
# http://s1.default.svc.cluster.local
def add_param_to_work_model(model, name_space, cluster_domain, image):
    for service in model:
        model[service].update({"url": f"http://{service}.{name_space}.svc.{cluster_domain}.local"})
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

        with open(f"yamls/{YAML_OUTPUT_FILE}-{service}.yaml", 'w') as file:
            file.write(f)
    print("Deployment Created!")

def create_configmap_yaml(mesh, model):
    with open('ConfigMapTemplate.yaml', 'r') as file:
        f = file.read()
        f = f.replace("{{SERVICE_MESH}}", json.dumps(mesh))
        f = f.replace("{{WORK_MODEL}}", json.dumps(model))

    with open("yamls/ConfigMapMicroSevice.yaml", 'w') as file:
        file.write(f)

    print("ConfigMap Created!")

add_param_to_work_model(work_model, NAMESPACE, CLUSTER_DOMAIN, IMAGE)

create_deployment_yaml_files(work_model, var_to_be_replaced)

create_configmap_yaml(service_mesh, work_model)
