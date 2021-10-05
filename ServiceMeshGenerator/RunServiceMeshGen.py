import errno
from ServiceMeshGenerator import get_service_mesh, SERVICEMESH_PATH
import json
from pprint import pprint
import sys
import os
import shutil

import argparse
import argcomplete


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The ServiceMesh Parameters file', default=f'{SERVICEMESH_PATH}/ServiceMeshParameters.json')

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

# if len(sys.argv) > 1:
#     parameters_file_path = sys.argv[1]
# elif len(SERVICEMESH_PATH) > 0:
#     parameters_file_path = f'{SERVICEMESH_PATH}/ServiceMeshParameters.json'
# else:
#     parameters_file_path = 'ServiceMeshParameters.json'

try:
    with open(parameters_file_path) as f:
        params = json.load(f)
    graph_parameters = params['ServiceMeshParameters']
    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = SERVICEMESH_PATH
    if "OutputFile" in params.keys() and len(params["OutputFile"]) > 0:
        output_file = params["OutputFile"]
    else:
        output_file = "servicemesh.json"
except Exception as err:
    print("ERROR: in RunServiceMeshGen,", err)
    exit(1)

output_file_png = f'{os.path.splitext(output_file)[0]}.png'
servicemesh = get_service_mesh(graph_parameters, output_path, output_file_png)

pprint(servicemesh)

# keyboard_input = input("Save service mesh on file? (y) ") or "y"
keyboard_input = "y"
if keyboard_input == "y":
    with open(f'{output_path}/{output_file}', "w") as f:
        f.write(json.dumps(servicemesh, indent=2))

    #if parameters_file_path != f"{output_path}/{os.path.basename(parameters_file_path)}":
    #    shutil.copyfile(parameters_file_path, f"{output_path}/{os.path.basename(parameters_file_path)}")

    print(f"'{output_path}/{output_file}'")
    print(f"'{output_path}/{output_file_png}'")
    print("Files Saved!")
