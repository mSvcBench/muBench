from K8sYamlBuilder import customization_work_model, create_deployment_yaml_files, K8s_YAML_BUILDER_PATH
import json
from pprint import pprint


try:
    with open(f'{K8s_YAML_BUILDER_PATH}/K8sParameters.json') as f:
        params = json.load(f)

    k8s_parameters = params["K8sParameters"]
    work_model_path = params['WorkModelPath']
    nfs_conf = params['NFSConfigurations']
except Exception as err:
    print("ERROR: in RunK8sYamlBuilder,", err)
    exit(1)

with open(work_model_path, "r") as f:
    work_model = json.load(f)

customization_work_model(work_model, k8s_parameters)

pprint(work_model)

with open(work_model_path, "w") as f:
    f.write(json.dumps(work_model))

create_deployment_yaml_files(work_model, k8s_parameters, nfs_conf)