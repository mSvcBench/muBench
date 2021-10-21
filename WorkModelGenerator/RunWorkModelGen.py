from WorkModelGenerator import get_work_model, WORKMODEL_PATH
import json
from pprint import pprint
import sys
import os
import shutil

import argparse
import argcomplete


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The WorkModel Parameters file', default=f'{WORKMODEL_PATH}/WorkModelParameters.json')

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

parameters_file_path = args.parameters_file

try:
    with open(parameters_file_path) as f:
        params = json.load(f)
    workmodel_parameters = params["WorkModelParameters"]
    servicemesh_file_path = workmodel_parameters["ServiceMeshFilePath"]["value"]
    with open(servicemesh_file_path) as f:
        servicemesh = json.load(f)
    if "OutputPath" in workmodel_parameters.keys() and len(workmodel_parameters["OutputPath"]["value"]) > 0:
        output_path = workmodel_parameters["OutputPath"]["value"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = WORKMODEL_PATH
    if "OutputFile" in workmodel_parameters.keys() and len(workmodel_parameters["OutputFile"]["value"]) > 0:
        output_file = workmodel_parameters["OutputFile"]["value"]
    else:
        output_file = "workmodel.json"
except Exception as err:
    print("ERROR: in creation of workmodel,", err)
    exit(1)

workmodel = get_work_model(servicemesh, workmodel_parameters)
pprint(workmodel)

# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    with open(f"{output_path}/{output_file}", "w") as f:
        f.write(json.dumps(workmodel, indent=2))

    #if parameters_file_path != f"{output_path}/{os.path.basename(parameters_file_path)}":
    #    shutil.copyfile(parameters_file_path, f"{output_path}/{os.path.basename(parameters_file_path)}")

    print(f"'{output_path}/{output_file}'")
    print("File Saved!")
