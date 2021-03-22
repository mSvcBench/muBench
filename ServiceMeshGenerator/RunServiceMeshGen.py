from ServiceMeshGenerator import get_service_mesh, pprint, json

# INPUT params:
graph_params_test = {"services_groups": 1, "vertices": 10, "power": 5, "edges_per_vertex": 2, "zero_appeal": 1,
                     "dbs": {"sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2}
                     }
####################


servicemesh = get_service_mesh(graph_params_test)

pprint(servicemesh)

keyboard_input = input("Save service mesh on file? (y)") or "y"

if keyboard_input == "y":
    with open("servicemesh.json", "w") as f:
        f.write(json.dumps(servicemesh))
