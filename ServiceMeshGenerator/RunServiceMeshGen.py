import errno
from ServiceMeshGenerator import get_service_mesh, SERVICEMESH_PATH
import json
from pprint import pprint
import sys
import os
import shutil


if len(sys.argv) > 1:
    parameters_file_path = sys.argv[1]
else:
    parameters_file_path = f'{SERVICEMESH_PATH}/ServiceMeshParameters.json'

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
except Exception as err:
    print("ERROR: in RunServiceMeshGen,", err)
    exit(1)


servicemesh = get_service_mesh(graph_parameters, output_path)

pprint(servicemesh)

# keyboard_input = input("Save service mesh on file? (y) ") or "y"
keyboard_input = "y"
if keyboard_input == "y":
    with open(f'{output_path}/servicemesh.json', "w") as f:
        f.write(json.dumps(servicemesh, indent=2))

    if output_path != SERVICEMESH_PATH:
        shutil.copy(parameters_file_path, f"{output_path}/")

    print(f"'{output_path}/servicemesh.json'")
    print(f"'{output_path}/servicemesh.png'")
    print("Files Saved!")
