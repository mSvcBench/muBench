from igraph import *
import json
from pprint import pprint
import random

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
graph_params_test = {"services_groups": 1, "vertices": 10, "power": 1, "edges_per_vertex": 1, "zero_appeal": 10,
                     # "dbs": {}
                     # "dbs": {"nodb": 1, "sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2}
                     # "dbs": {"sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2}
                     }

SERVICEMESH_PATH = os.path.dirname(__file__)


def select_db(dbs):
    dbs_items = dbs.items()
    random_extraction = random.random()
    # print("Extraction: %.4f" % random_extraction)
    p_total = 0.0
    for p_db in dbs.values():
        p_total += p_db
    p_total = round(p_total, 10)
    prev_interval = 0
    for db in dbs_items:
        if random_extraction <= prev_interval + db[1]/p_total:
            return db[0]
        prev_interval += round(db[1]/p_total, 10)


def edges_reversal(graph):
    for edge in graph.get_edgelist():
        graph.delete_edges([(edge[0], edge[1])])
        graph.add_edges([(edge[1], edge[0])])


def get_service_mesh(graph_params):
    # Takes as inputs the graph parameters and generates its json file accordingly
    g = Graph.Barabasi(n=graph_params["vertices"], power=graph_params["power"], m=graph_params["edges_per_vertex"],
                       zero_appeal=graph_params["zero_appeal"], directed=True)
    g.vs["label"] = list(range(graph_params["vertices"]))  # label nodes with

    edges_reversal(g)
    # print("PRIMA", g)
    service_mesh = {}

    graph_added_dbs = list()
    for vertex in range(graph_params["vertices"]):
        service_list = []
        service_list_dict = {}

        for services_group_id in range(graph_params["services_groups"]):
            service_list_dict["services"] = [f"s{service}" for service in g.get_adjlist()[vertex]]
            service_list_dict["seq_len"] = len(service_list_dict["services"])

            if service_list_dict["seq_len"] != 0:
                service_list.append(service_list_dict)

            service_mesh[f"s{vertex}"] = service_list

        if "dbs" in graph_params.keys() and len(graph_params["dbs"]) > 0:
            selected_db = select_db(graph_params["dbs"])
            # print(selected_db)
            if selected_db == "nodb":
                continue
            if selected_db not in graph_added_dbs:
                graph_added_dbs.append(selected_db)
                g.add_vertices(1)
                service_mesh[selected_db] = list()
            new_vertex = g.vcount() - 1
            g.add_edges([(vertex, new_vertex)])
            service_mesh[f"s{vertex}"].append({'seq_len': 1, "services": [selected_db]})

    # print("THE MESH:\n", json.dumps(service_mesh))

    g.vs["label"] = list(range(graph_params["vertices"])) + graph_added_dbs
    g.vs["size"] = 35
    plot(g, f"{SERVICEMESH_PATH}/servicemesh.png")
    # print(g)
    print("Service Mesh Created!")
    return service_mesh


# pprint(get_service_mesh(graph_params_test))
# get_service_mesh(graph_params_test)
# db_param_test = {"sdb1": 0.4,
#                  "sdb2": 0.6,
#                  "sdb3": 0.2
#                  }
# print(select_db(db_param_test))