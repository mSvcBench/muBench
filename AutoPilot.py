import ServiceMeshGenerator.ServiceMeshGenerator as smGen
import WorkModelGenerator.WorkModelGenerator as wmGen
import WorkLoadGenerator.WorkLoadGenerator as wlGen
from Kubernetes.K8sYamlBuilder import K8sYamlBuilder as K8sBuilder
from Kubernetes.K8sDeployer import K8sDeployer as K8sDeployer
import os
import json
import shutil
import AutoPilotConf as APConf


############### Input Param ###############
##### ServiceMesh Params
vertices = APConf.vertices
services_groups = APConf.services_groups  # Number of services for group
power = APConf.power  # Power ???
edges_per_vertex = APConf.edges_per_vertex
zero_appeal = APConf.zero_appeal
dbs = APConf.dbs


##### WorkModel Params
# Possible Internal Job Functions with params
work_model_params = APConf.work_model_params


##### Workload
ingress_dict = APConf.ingress_dict  # Dictionary of possibile ingress Services with associated probability
min_services = APConf.min_services  # MIN number of selected ingress dictionary
max_services = APConf.max_services  # MAX number of selected ingress dictionary

stop_event = APConf.stop_event  # Number of event until the end of simulation
mean_interarrival_time = APConf.mean_interarrival_time  # Mean of request interarrival

#### K8s Yaml Builder

prefix_yaml_output_file = APConf.prefix_yaml_output_file
deployment_namespace = APConf.deployment_namespace
image_name = APConf.image_name
cluster_domain = APConf.cluster_domain
service_path = APConf.service_path
# var_to_be_replaced = {"{{string_in_template}}": "new_value", ...}
var_to_be_replaced = APConf.var_to_be_replaced
nfs_conf = APConf.nfs_conf

#### Autopilot
job_functions_file_path = APConf.job_functions_file_path

###########################
##          RUN          ##
###########################

print(K8sBuilder.K8s_YAML_BUILDER_PATH)
folder_not_exist = False
if not os.path.exists(f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"):
    folder_not_exist = True
folder = f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"


def create_deployment_config():
    print("---")
    service_mesh_params = {"services_groups": services_groups,
                           "vertices": vertices,
                           "power": power,
                           "edges_per_vertex": edges_per_vertex,
                           "zero_appeal": zero_appeal,
                           "dbs": dbs
                           }
    servicemesh = smGen.get_service_mesh(service_mesh_params)

    workmodel = wmGen.get_work_model(servicemesh, work_model_params)

    K8sBuilder.customization_work_model(workmodel, service_path, deployment_namespace, cluster_domain, image_name)
    K8sBuilder.create_deployment_yaml_files(workmodel, prefix_yaml_output_file, nfs_conf, deployment_namespace, var_to_be_replaced)
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


def copy_config_file_to_nfs(nfs_folder_path, servicemesh, workmodel, job_functions):
    try:
        with open(f"{nfs_folder_path}/servicemesh.json", "w") as f:
            f.write(json.dumps(servicemesh))

        with open(f"{nfs_folder_path}/workmodel.json", "w") as f:
            f.write(json.dumps(workmodel))

        if os.path.exists(f"{smGen.SERVICEMESH_PATH}/servicemesh.json"):
            # TODO Implementare copia della service mesh nel path dell'NFS server
            print(":)")

        if job_functions != "" or job_functions is None:
            if not os.path.exists(f"{nfs_folder_path}/JobFunctions"):
                os.makedirs(f"{nfs_folder_path}/JobFunctions")

            if os.path.isdir(job_functions):
                src_files = os.listdir(job_functions)
                for file_name in src_files:
                    full_file_name = os.path.join(job_functions, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, f"{nfs_folder_path}/JobFunctions/")
            else:
                shutil.copyfile(job_functions, f"{nfs_folder_path}/JobFunctions/{job_functions}")
                print("FILE")

    except Exception as er:
        print("Error in copy_config_file_to_nfs: %s" % er)
        exit()


######## SCRIPT
# try:
if folder_not_exist or len(os.listdir(folder)) == 0:

    keyboard_input = input("\nDirectory empty, wanna DEPLOY? (y)").lower() or "y"

    if keyboard_input == "y" or keyboard_input == "yes":
        updated_folder_items, service_mesh, work_model = create_deployment_config()
        copy_config_file_to_nfs(nfs_folder_path=nfs_conf["mount_path"], servicemesh=service_mesh,
                                workmodel=work_model, job_functions=job_functions_file_path)

        # pprint(service_mesh)
        # pprint(work_model)

        # deploy_items(updated_folder_items)
        K8sDeployer.deploy_volume(f"{folder}/PersistentVolumeMicroService.yaml")
        K8sDeployer.deploy_nginx_gateway(folder)
        K8sDeployer.deploy_items(folder)

        keyboard_input = input("Do you wanna create the workload file?? (y)  ") or "y"
        if keyboard_input == "y" or keyboard_input == "yes":
            req_params = {"stop_event": stop_event, "mean_interarrival_time": mean_interarrival_time}
            workload = wlGen.get_workload(ingress_dict, {"min": min_services, "max": max_services}, req_params)
            with open(f"WorkLoadGenerator/workload.json", "w") as f:
                f.write(json.dumps(workload))
            print("Worklod file saved in '%s'" % os.path.abspath("workload.json"))

    else:
        print("...\nOk you do not want to DEPLOY stuff! Bye!")
else:
    print("######################")
    print("!!!! Warning !!!!")
    print("######################")
    print(f"Folder is not empty: {folder}.")
    keyboard_input = input("Wanna UNDEPLOY old yamls first, delete the files and then start again? (n) ") or "n"
    if keyboard_input == "y" or keyboard_input == "yes":
        K8sDeployer.undeploy_items(folder)
        K8sDeployer.undeploy_nginx_gateway(folder)
        K8sDeployer.undeploy_volume(f"{folder}/PersistentVolumeMicroService.yaml")
        remove_files(folder)

    else:
        print("...\nOk you want to keep the OLD deployment! Bye!")

# except Exception as err:
#     print("######################")
#     print(f"Exception in 'main': {err}")
#     print("######################")
# except KeyboardInterrupt:
#     print("\n...\nBye bye!")

