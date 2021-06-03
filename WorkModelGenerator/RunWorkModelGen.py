from WorkModelGenerator import get_work_model, WORKMODEL_PATH
import json
from pprint import pprint
import sys
import os

if len(sys.argv) > 1:
    parameters_file_path = sys.argv[1]
else:
    parameters_file_path = f'{WORKMODEL_PATH}/ServiceMeshParameters.json'

try:
    with open(f'{WORKMODEL_PATH}/WorkModelParameters.json') as f:
        params = json.load(f)
    workmodel_parameters = params['WorkModelParameters']
    servicemesh_file_path = params['ServiceMeshFilePath']
    with open(servicemesh_file_path) as f:
        servicemesh = json.load(f)
    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = WORKMODEL_PATH
except Exception as err:
    print("ERROR: in creation of service mesh,", err)
    exit(1)

workmodel = get_work_model(servicemesh, workmodel_parameters)
pprint(workmodel)

# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    with open(f"{output_path}/workmodel.json", "w") as f:
        f.write(json.dumps(workmodel))

    print(f"'{output_path}/workmodel.json'")
    print("File Saved!")
