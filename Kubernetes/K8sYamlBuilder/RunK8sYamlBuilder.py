from K8sYamlBuilder import customization_work_model, create_deployment_yaml_files, json, pprint

# INPUT params:
PREFIX_YAML_FILE = "MicroServiceDeployment"
NAMESPACE = "default"
IMAGE = "lucapetrucci/microservice:latest"
CLUSTER_DOMAIN = "cluster"
PATH = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

work_model_path = "../../WorkModelGenerator/workmodel.json"

####################


with open(work_model_path, "r") as f:
    work_model = json.load(f)

customization_work_model(work_model, PATH, NAMESPACE, CLUSTER_DOMAIN, IMAGE)
pprint(work_model)

create_deployment_yaml_files(work_model, PREFIX_YAML_FILE, var_to_be_replaced)
