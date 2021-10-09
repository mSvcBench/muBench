import sys
import os
import json
import shutil
# appending a path
sys.path.append('../../')

import K8sYamlBuilder as K8sYamlBuilder
import K8sYamlDeployer as K8sYamlDeployer

import argparse
import argcomplete


### Functions
def create_deployment_config():
    print("---")
    try:
        with open(workmodel_path) as f:
            workmodel = json.load(f)
    except Exception as err:
        print("ERROR: in RunK8sDeployer,", err)
        exit(1)
    K8sYamlBuilder.customization_work_model(workmodel, k8s_parameters)
    K8sYamlBuilder.create_deployment_yaml_files(workmodel, k8s_parameters, nfs_conf, builder_module_path)
    created_items = os.listdir(f"{builder_module_path}/yamls")
    print(f"The following files are created: {created_items}")
    print("---")
    # return a list of the files just created
    return created_items, workmodel

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


def copy_config_file_to_nfs(nfs_folder_path, workmodel, internal_service_functions):
    try:
        # Remove NFS mub folder contents
        if os.path.exists(nfs_folder_path):
            shutil.rmtree(nfs_folder_path,ignore_errors=True)
            os.makedirs(nfs_folder_path)
            os.makedirs(f"{nfs_folder_path}/InternalServiceFunctions")
        
        if output_path is None:
            with open(f"{nfs_folder_path}/workmodel.json", "w") as f:
                f.write(json.dumps(workmodel, indent=2))
        else:
            with open(f"{output_path}/workmodel.json", "w") as f:
                f.write(json.dumps(workmodel, indent=2))

            shutil.copy(f"{output_path}/workmodel.json", f"{nfs_folder_path}/")

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
                shutil.copyfile(internal_service_functions, f"{nfs_folder_path}/InternalServiceFunctions/{internal_service_functions.split('/')[-1]}")
                print("FILE")

    except Exception as er:
        print("Error in copy_config_file_to_nfs: %s" % er)
        exit()

### Main

k8s_Builder_PATH = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The K8s Parameters file', default=f'{k8s_Builder_PATH}/K8sParameters.json')

argcomplete.autocomplete(parser)

try:
    args = parser.parse_args()
except ImportError:
    print("Import error, there are missing dependencies to install.  'apt-get install python3-argcomplete "
          "&& activate-global-python-argcomplete3' may solve")
except AttributeError:
    parser.print_help()
except Exception as err:
    print("Error:", err)

#### input params
parameters_file_path = args.parameters_file

try:
    with open(parameters_file_path) as f:
        params = json.load(f)

    k8s_parameters = params["K8sParameters"]
    nfs_conf = params['NFSConfigurations']
    internal_service_functions_file_path = params['InternalServiceFilePath']
    workmodel_path = params['WorkModelPath'] 

    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = None

except Exception as err:
    print("ERROR: in RunK8sDeployer,", err)
    exit(1)


###  Create YAML, insert files (workmodel.json and custom function) in k8s NFS and deploy YAML 

folder_not_exist = False
if output_path is None:
    builder_module_path = K8sYamlBuilder.K8s_YAML_BUILDER_PATH
else:
    builder_module_path = output_path
if not os.path.exists(f"{builder_module_path}/yamls"):
    folder_not_exist = True
folder = f"{builder_module_path}/yamls"

if parameters_file_path != f"{output_path}/{os.path.basename(parameters_file_path)}":
    shutil.copyfile(parameters_file_path, f"{output_path}/{os.path.basename(parameters_file_path)}")

if folder_not_exist or len(os.listdir(folder)) == 0:

    # keyboard_input = input("\nDirectory empty, wanna DEPLOY? (y)").lower() or "y"
    keyboard_input = "y"

    if keyboard_input == "y" or keyboard_input == "yes":
        updated_folder_items, work_model = create_deployment_config()   # Creates YAML files
        copy_config_file_to_nfs(nfs_folder_path=nfs_conf["mount_path"], 
            workmodel=work_model, internal_service_functions=internal_service_functions_file_path) # Insert files in NFS

        # Deploy YAML files
        K8sYamlDeployer.deploy_volume(f"{folder}/PersistentVolumeMicroService.yaml")
        K8sYamlDeployer.deploy_nginx_gateway(folder)
        K8sYamlDeployer.deploy_items(folder)
    else:
        print("...\nOk you do not want to DEPLOY stuff! Bye!")
else:
    print("######################")
    print("!!!! Warning !!!!")
    print("######################")
    print(f"Folder is not empty: {folder}.")
    keyboard_input = input("Wanna UNDEPLOY old yamls first, delete the files and then start again? (n) ") or "n"
    if keyboard_input == "y" or keyboard_input == "yes":
        K8sYamlDeployer.undeploy_items(folder)
        K8sYamlDeployer.undeploy_nginx_gateway(folder)
        K8sYamlDeployer.undeploy_volume(f"{folder}/PersistentVolumeMicroService.yaml")
        remove_files(folder)

    else:
        print("...\nOk you want to keep the OLD deployment! Bye!")

