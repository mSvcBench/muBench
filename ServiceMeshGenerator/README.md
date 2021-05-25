# Service Mesh Generator
The ServiceMeshGenerator generates a file that descibes the mesh of the microservice that links the services throughout the Microservice Application.

Studies have shown that the interconnetions between services among real microservice applications follow a power-law distribution that can be modelled using a Barabási-Albert (BA) model.
For this reason we chose to model the service mesh as a BA graph.
If we play with the values of the BA model, we are able to genereate microservice applications with different topologies. 

First, we describe the parameters, then we show 4 different topologies taken from the following [reaserch paper](https://researchcommons.waikato.ac.nz/bitstream/handle/10289/13981/EVOKE_CASCON_2020_paper_37_WeakestLink.pdf?sequence=11&isAllowed=y).


## Install requirements
First, install the requirements using ``pip``:

```zsh
pip3 install -r requirements.txt
```

## Edit input parameters:
Next, edit the ``RunServiceMeshGen.py`` before running it.
It is important to edit the `graph_parameters` parameter, as it describes the generating process of the service mesh.
In particular:

* `services_groups` indicates how many groups of services can be executed in parallel while performing the simulations 
* `vertices` are the number of vertices a service mesh has (db excluded, more later)
* `power` is the exponent of the power law distribution that defines the generation of the service mesh. Essentially, an high value of this parameter imply an higher probability that one vertex is connected to more vertices, on the other hand, a lower value of the parameter means a lower chance a vertex is connected to other vertices.

* `zero_appeal` is the attractiveness of vertices with no edges, meaning, it is the probability that during the creation of the topology, a new node is linked to a vertex with no outgoing edges.

* `dbs` is used to specify if the service mesh is generated with services that behave as databases. 
You can specify a list of db names followed by the probability it can be chosen by the services.
Three options are possible:
    1. `"dbs": {}` there are no db services inside the mesh 
    1. `"dbs": {"sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2}` every service is attached to one of the listed dbs
    1. `"dbs": {"nodb": 1, "sdb1": 0.4, "sdb2": 0.6, "sdb3": 0.2, ...}` similar to the previous example but with the possibility that a service can be attached to none of the listed dbs thanks to the `nodb` probability.

Now, we illustrate four examples of different service mesh topologies:

* An highly-centralized hierarchical architectures with most of the services linked to one service (exluded the db services):

```
graph_parameters = {"services_groups": 1, "vertices": 10, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 0.01,
                     "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}}
```

<img width="400" height="400" src="../Docs/service_mesh_example_1.png">

*  An applications that rely on a common logging service


```
graph_parameters = {"services_groups": 1, "vertices": 10, "power": 0.9, "edges_per_vertex": 1, "zero_appeal": 0.01,
                     "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}}
```

<img width="400" height="400" src="../Docs/service_mesh_example_2.png">

* An application with several auxiliary services:


```
graph_parameters = {"services_groups": 1, "vertices": 10, "power": 0.05, "edges_per_vertex": 1, "zero_appeal": 3.25,
                     "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}}
```

<img width="400" height="400" src="../Docs/service_mesh_example_3.png">

* An application organized in the conventional multi-tier fashion:

```
graph_parameters = {"services_groups": 1, "vertices": 10, "power": 0.9, "edges_per_vertex": 1, "zero_appeal": 3.25,
                     "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}}
```

<img width="400" height="400" src="../Docs/service_mesh_example_4.png">


---
## Run the script
Finally, to run only the ServiceMeshGenerator, run the script:

```
python3 RunServiceMeshGen.py
```