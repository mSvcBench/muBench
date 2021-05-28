import ServiceMeshGenerator.ServiceMeshGenerator as smGen
import WorkModelGenerator.WorkModelGenerator as wmGen
import WorkLoadGenerator.WorkLoadGenerator as wlGen
from Kubernetes.K8sYamlBuilder import K8sYamlBuilder as K8sBuilder
from Kubernetes.K8sDeployer import K8sDeployer as K8sDeployer
import os
import json
import shutil

try:
    with open('AutoPilotConf.json') as f:
        params = json.load(f)

    ############### Input Param ###############
    ##### ServiceMesh Params
    graph_parameters = params['ServiceMeshParameters']

    ##### WorkModel Params
    workmodel_parameters = params['WorkModelParameters']

    #### K8s Yaml Builder
    k8s_parameters = params["K8sParameters"]
    nfs_conf = params['NFSConfigurations']

    ##### Workload
    workload_parameters = params['WorkLoadParameters']

    #### Autopilot
    internal_service_functions_file_path = params['InternalServiceFilePath']


except Exception as err:
    print("ERROR: in RunWorkLoadGen,", err)
    exit(1)

###########################
##          RUN          ##
###########################

folder_not_exist = False
if not os.path.exists(f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"):
    folder_not_exist = True
folder = f"{K8sBuilder.K8s_YAML_BUILDER_PATH}/yamls"


def create_deployment_config():
    print("---")

    servicemesh = smGen.get_service_mesh(graph_parameters)

    workmodel = wmGen.get_work_model(servicemesh, workmodel_parameters)

    K8sBuilder.customization_work_model(workmodel, k8s_parameters)

    K8sBuilder.create_deployment_yaml_files(workmodel, k8s_parameters, nfs_conf)

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


def copy_config_file_to_nfs(nfs_folder_path, servicemesh, workmodel, internal_service_functions):
    try:
        with open(f"{nfs_folder_path}/servicemesh.json", "w") as f:
            f.write(json.dumps(servicemesh))

        with open(f"{nfs_folder_path}/workmodel.json", "w") as f:
            f.write(json.dumps(workmodel))

        if os.path.exists(f"{smGen.SERVICEMESH_PATH}/servicemesh.png"):
            shutil.copy(f"{smGen.SERVICEMESH_PATH}/servicemesh.png", f"{nfs_folder_path}/")

        if internal_service_functions != "" or internal_service_functions is None:
            if not os.path.exists(f"{nfs_folder_path}/InternalServiceFunctions"):
                os.makedirs(f"{nfs_folder_path}/InternalServiceFunctions")

            if os.path.isdir(internal_service_functions):
                src_files = os.listdir(internal_service_functions)
                for file_name in src_files:
                    full_file_name = os.path.join(internal_service_functions, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, f"{nfs_folder_path}/InternalServiceFunctions/")
            else:
                shutil.copyfile(internal_service_functions, f"{nfs_folder_path}/InternalServiceFunctions/{internal_service_functions}")
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
                                workmodel=work_model, internal_service_functions=internal_service_functions_file_path)

        # pprint(service_mesh)
        # pprint(work_model)

        # deploy_items(updated_folder_items)
        K8sDeployer.deploy_volume(f"{folder}/PersistentVolumeMicroService.yaml")
        K8sDeployer.deploy_nginx_gateway(folder)
        K8sDeployer.deploy_items(folder)

        keyboard_input = input("Do you wanna create the workload file?? (y)  ") or "y"
        if keyboard_input == "y" or keyboard_input == "yes":
            workload = wlGen.get_workload(workload_parameters)
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

