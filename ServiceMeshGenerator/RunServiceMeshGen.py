import errno
from ServiceMeshGenerator import get_service_mesh, pprint, json

try:
    params = json.loads("ServiceMeshParameters.json")
    graph_parameters = params['ServiceMeshParameters']
except Exception as err:
    print("ERROR: in creation of service mesh,", err)
    exit(1)
        
servicemesh = get_service_mesh(graph_parameters)

pprint(servicemesh)

keyboard_input = input("Save service mesh on file? (y)") or "y"

if keyboard_input == "y":
    with open("servicemesh.json", "w") as f:
        f.write(json.dumps(servicemesh))
