from igraph import *
import random
import os

SERVICEMESH_PATH = os.path.dirname(os.path.abspath(__file__))

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


def get_service_mesh(graph_params, output_path=None):
    if output_path is None:
        output_path = SERVICEMESH_PATH
    # Takes as inputs the graph parameters and generates its json file accordingly
    g = Graph.Barabasi(n=graph_params["vertices"], power=graph_params["power"], m=1,
                       zero_appeal=graph_params["zero_appeal"], directed=True)
    g.vs["label"] = list(range(graph_params["vertices"]))  # label nodes with

    edges_reversal(g)
    service_mesh = {}

    graph_added_dbs = list()
    for vertex in range(graph_params["vertices"]):
        service_list = []

        current_service_group = 0
        # print("vertex: %d -> childs: " %vertex, g.get_adjlist()[vertex])
        for service_id in g.get_adjlist()[vertex]:
            if len(service_list) == current_service_group:
                service_list.append({"seq_len": graph_params["seq_len"], "services": list()})

            service_list[current_service_group]["services"].append(f"s{service_id}")
            current_service_group = (current_service_group + 1) % graph_params["external_service_groups"]
                
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
    plot(g, f"{output_path}/servicemesh.png")
    # print(g)
    print("Service Mesh Created!")
    return service_mesh
