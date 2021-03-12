from K8sYamlBuilder import customization_work_model, create_deployment_yaml_files, json, pprint

# INPUT params:
prefix_yaml_file = "MicroServiceDeployment"
namespace = "default"
image = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
path = "/api/v1"
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = {}

nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}

work_model_path = "../../WorkModelGenerator/workmodel.json"

####################


with open(work_model_path, "r") as f:
    work_model = json.load(f)

customization_work_model(work_model, path, namespace, cluster_domain, image)

pprint(work_model)

with open(work_model_path, "w") as f:
    f.write(json.dumps(work_model))


create_deployment_yaml_files(work_model, prefix_yaml_file, nfs_conf, namespace, var_to_be_replaced)
