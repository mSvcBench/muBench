# Configure MicroServiceSimulator from scratch

In this file we describe the necessary step to run the MicroService Simulator from scratch.

Se non tocchi nulla genera un'app composta da 5 servizi

```shell
export NFS_SHARED_FOLDER="/mnt/MSSharedData" 
```

## 1. Generate the service mesh that represent the MicroService
We start with the generation of the service mesh.

```shell
cd MicroServiceSimulator/ServiceMeshGenerator
```
* Edit the input parameters in the top of file `RunServiceMeshGen.py`, if you wish

```python
graph_params_test = {"services_groups": 1,  
                     "vertices": 5, 
                     "power": 1, 
                     "edges_per_vertex": 1, 
                     "zero_appeal": 10
                    }
```
* Then run the python file `RunServiceMeshGen.py`
```shell
python RunServiceMeshGen.py
```
* When the pyhton programm ask for savig the `servicemesh.json` file type `y`, 
now we have to copy this file in the NFS shared folder.
```shell
cp servicemesh.json $NFS_SHARED_FOLDER/
```

## 2. Generate the work model of the MicroService
The second step goal is to create the work model for the MicroService application, 
you can assign which job a service must execute when called.

```shell
cd MicroServiceSimulator/WorkModelGenerator
```
In a similar way to step one: 
* Edit the input parameters in the top of file `RunWorkModelGen.py`.
Pay attenction that the variable `v_numbers` must have the same value of the `graph_params_test["vertices"]`  in the step one.
Se vuoi aggiungere funzioni custom guarda il  file giusto

```python
v_numbers = 5
parameters = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [1, 250]}
             }
```
* Run the python file `RunServiceMeshGen.py`
```shell
python RunWorkModelGen.py
```
* Per la copia aspettiamo, il file verrà modificato allo step 3 

## 3. Build yaml files for the Kubernetes deployment

As a result, the K8s Yaml Builder creates, on the `MicroServiceSimulator/Kubernetes/K8sYamlBuilder/yamls` path, one YAML per service with its `Deployment` and its relating `Service`, along with other files useful for the overall deployment of the MSS.

```shell
cd MicroServiceSimulator/Kubernetes/K8sYamlBuilder
```

* Edit the parameters in `RunK8sYamlBuilder.py` file. You must edit the `nfs_conf` parmas with the correct address and shared folder path of the NFS server.
```python
prefix_yaml_file = "MicroServiceDeployment"
namespace = "default"
image = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
path = "/api/v1"
var_to_be_replaced = {}  # e.g. {"{{string_in_template}}": "new_value", ...}
nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}
work_model_path = "../../WorkModelGenerator/workmodel.json"
```
* Run the python file `RunK8sYamlBuilder.py`, this programm edit the workmodel.json files and create all the necessary yaml files to deploy the MicroService Simulator on K8s.
```shell
python RunK8sYamlBuilder.py
```
* Copy the updated `workmodel.json` file in the NFS shared folder. 
```shell
cp workmodel.json $NFS_SHARED_FOLDER/
```
* Applica tutto
```shell
kubectl apply -f yamls
```
