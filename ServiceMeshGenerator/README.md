# Service Mesh Generator

If you want to learn theoretical insights of the *Service Mesh Generator* [go here](/Docs/BuildingTools.md#Service-Mesh-Generator), otherwise, if you want to run it, go through the following steps.


---
## Install requirements
First, install the requirements using ``pip3``:

```zsh
pip3 install -r requirements.txt
```

---
## Run the script
Edit the `ServiceMeshParameters.json` file before running the `ServiceMeshGenerator`.

Finally, run the script to obtain `servicemesh.json` and `servicemesh.png` as follows:

```zsh
python3 RunServiceMeshGen.py
```

## Examples
We illustrate four examples of different service mesh topologies:

* An highly-centralized hierarchical architectures with most of the services linked to one service (excluded the db services):

```json
{
    "external_service_groups": 1, 
    "vertices": 10, 
    "power": 0.05,
    "zero_appeal": 0.01,
    "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}
}
```

<img width="400" src="../Docs/service_mesh_example_1.png">

*  An applications that rely on a common logging service


```json
{
    "external_service_groups": 1, 
    "vertices": 10, 
    "power": 0.9,
    "zero_appeal": 0.01,
    "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}
}
```

<img width="400" src="../Docs/service_mesh_example_2.png">

* An application with several auxiliary services:


```json
{
    "external_service_groups": 1,
    "vertices": 10, 
    "power": 0.05, 
    "zero_appeal": 3.25,
    "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}
}
```

<img width="400" src="../Docs/service_mesh_example_3.png">

* An application organized in the conventional multi-tier fashion:

```json
{
    "external_service_groups": 1, 
    "vertices": 10, 
    "power": 0.9,  
    "zero_appeal": 3.25,
    "dbs": {"nodb": 0.2, "sdb1": 0.6, "sdb2": 0.4}
}
```

<img width="400" src="../Docs/service_mesh_example_4.png">
