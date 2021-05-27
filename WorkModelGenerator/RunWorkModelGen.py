from WorkModelGenerator import get_work_model, WORKMODEL_PATH
import json
from pprint import pprint

try:
    with open(f'{WORKMODEL_PATH}/WorkModelParameters.json') as f:
        params = json.load(f)
    workmodel_parameters = params['WorkModelParameters']
    servicemesh_file_path = params['ServiceMeshFilePath']
    with open(servicemesh_file_path) as f:
        servicemesh = json.load(f)
except Exception as err:
    print("ERROR: in creation of service mesh,", err)
    exit(1)

workmodel = get_work_model(servicemesh, workmodel_parameters)
pprint(workmodel)

# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    with open(f"{WORKMODEL_PATH}/workmodel.json", "w") as f:
        f.write(json.dumps(workmodel))

    print(f"'{WORKMODEL_PATH}/workmodel.json'")
    print("File Saved!")
