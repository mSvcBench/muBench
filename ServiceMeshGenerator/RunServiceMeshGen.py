from ServiceMeshGenerator import get_service_mesh, pprint, json

# INPUT params:
# graph_params_test = {"services_groups": 1, "vertices": 10, "power": 1, "edges_per_vertex": 1, "zero_appeal": 10}
# graph_params_test = {"services_groups": 1, "vertices": 15, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 0.01} #1
# graph_params_test = {"services_groups": 1, "vertices": 15, "power": 0.9, "edges_per_vertex": 1, "zero_appeal": 0.01} #2
# graph_params_test = {"services_groups": 1, "vertices": 15, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 3.25} #3
# graph_params_test = {"services_groups": 1, "vertices": 15, "power": 0.9, "edges_per_vertex": 1, "zero_appeal": 3.25} #4
# graph_params_test = {"services_groups": 1, "vertices": 10, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 3.25,
#                      "dbs": {"sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2}
#                      }
graph_params_test = {"services_groups": 1, "vertices": 10, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 3.25,
                     "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}
                     # "dbs": {"sdb1": 0.6, "sdb2": 0.4}
                     }
####################


servicemesh = get_service_mesh(graph_params_test)

pprint(servicemesh)

keyboard_input = input("Save service mesh on file? (y)") or "y"

if keyboard_input == "y":
    with open("servicemesh.json", "w") as f:
        f.write(json.dumps(servicemesh))
