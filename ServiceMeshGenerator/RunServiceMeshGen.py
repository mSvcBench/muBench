from ServiceMeshGenerator import get_service_mesh, pprint, json

# INPUT params:
graph_params_test = {"services_groups": 1, "vertices": 10, "power": 1, "edges_per_vertex": 1, "zero_appeal": 10}

####################


servicemesh = get_service_mesh(graph_params_test)

pprint(servicemesh)

keyboard_input = input("Save service mesh on file? (y)") or "y"

if keyboard_input == "y":
    with open("servicemesh.json", "w") as f:
        f.write(json.dumps(servicemesh))
