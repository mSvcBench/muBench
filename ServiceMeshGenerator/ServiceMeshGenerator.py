from igraph import *
import json
from pprint import pprint

'''
{
  "s1": [
    {
      "seq_len": 3,
      "services": ["s2", "s3", "s5"]
    },
    {
      "seq_len": 2,
      "services": ["s5", "s3"]
    }
  ],
  "s2": [],
  "s3": [
    {
      "seq_len": 1,
      "services": ["s4"]
    }
  ],
  "s4": [],
  "s5": []
}
'''

# graph_params_test = {"services_groups": 1, "vertices": 10, "power": 0.9, "edges_per_vertex": 1, "zero_appeal": 0.001}
graph_params_test = {"services_groups": 1, "vertices": 10, "power": 1, "edges_per_vertex": 1, "zero_appeal": 10}


def get_service_mesh(graph_params):
    # Takes as inputs the graph parameters and generates its json file accordingly
    g = Graph.Barabasi(n=graph_params["vertices"], power=graph_params["power"], m=graph_params["edges_per_vertex"],
                       zero_appeal=graph_params["zero_appeal"], directed=True)
    g.vs["label"] = list(range(graph_params["vertices"]))  # label nodes with

    service_mesh = {}

    for vertex in range(graph_params["vertices"]):
        service_list = []
        service_list_dict = {}

        for services_group_id in range(graph_params["services_groups"]):
            service_list_dict["services"] = [f"s{service}" for service in g.get_adjlist()[vertex]]
            service_list_dict["seq_len"] = len(service_list_dict["services"])

            if service_list_dict["seq_len"] != 0:
                service_list.append(service_list_dict)

            service_mesh[f"s{vertex}"] = service_list

    # print("THE MESH:\n", json.dumps(service_mesh))

    # g.vs["label"] = list(range(graph_params["vertices"]))
    # print(g)
    # plot(g)
    print("Service Mesh Created!")
    return service_mesh

# pprint(get_service_mesh(graph_params_test))
