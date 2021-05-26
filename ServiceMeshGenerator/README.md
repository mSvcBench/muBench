# Service Mesh Generator
The ServiceMeshGenerator generates a .json file that descibes the service mesh of the Microservice Application.

## Service Mesh Topology
Litterature [studies](https://researchcommons.waikato.ac.nz/bitstream/handle/10289/13981/EVOKE_CASCON_2020_paper_37_WeakestLink.pdf?sequence=11&isAllowed=y) show that the building of a realistic mesh can be done by using the Barabási-Albert (BA) algorithm, which uses a power-law distribution and results in a topology that follows a preferential-attachment model. For this reason we chose to model the service mesh as a BA graph.
If we change the values of the BA model, we are able to genereate microservice applications with different mesh topologies. 

The BA algorithm builds the mesh topology as follows: at each step a new service is added as a vertex of a directed tree. This new service is connected with an edge to a single *parent* service already present in the topology. The edge direction is from the parent service to the new *child* service, this means that the parent service includes the new service in its external-services.  
The parent service is chosen according to a preferred attachment strategy using a power-law distribution. Specifically, vertex *i* is chosen as a parent with a (non-normalized) probability equal to *Pi = di^aplha+a*, where *di* is the number of services that have already chosen the service *i* as a parent, *alpha* is the power-law exponent, and *a* is the zero-appeal property i.e., the probability of a service being chosen as a parent when no other service has yet chosen it.

## Service Grouping
To simulate parallel and sequential execution of external-services, the whole set of external-services of a service is divided in a number of `services_groups`. Each group contains a different set of external-services and the insertion of external-services in groups is made according to a water-filling algorithm.

## Service calls
When a service request is received, a service executes its internal-service and then  

## Install requirements
First, install the requirements using ``pip``:

```zsh
pip3 install -r requirements.txt
```

## Edit input parameters:
Next, edit the values of the keys in ``ServiceMeshParameters.json`` before running the ``RunServiceMeshGen.py`` that actually generates the mesh files (servicemesh.json and servicemesh.png). The meaning of the keys is:

* `vertices` are the number of services that forms the microservice application (db excluded, more later)
* `power` is the exponent of the power law distribution that defines the generation of the service mesh. Essentially, an high value of this parameter imply an higher probability that one vertex is connected to more vertices, on the other hand, a lower value of the parameter means a lower chance a vertex is connected to other vertices.
* `zero_appeal` is the attractiveness of vertices with no edges, meaning, it is the probability that during the creation of the topology, a new node is linked to a vertex with no outgoing edges.
* `services_groups` indicates the number of groups in which the of external-services of a service are divided. 
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