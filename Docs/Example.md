# Configure MicroServiceSimulator from scratch

In this file we describe the necessary step to run the MicroService Simulator from scratch.
If you leave the files unchanged, it will generate a Microservice composed of 5 services.

Before we begin, export the path to your NFS shared folder as an environment variable.
```shell
export NFS_SHARED_FOLDER="/mnt/MSSharedData" 
```

## 1. Generate the service mesh that represent the MicroService
We start with the generation of the service mesh.

```shell
cd MicroServiceSimulator/ServiceMeshGenerator
```
* If you want to tune the parameters for the generation of the service mesh, edit the input parameters at the beginning of the `RunServiceMeshGen.py` file:

```python
graph_params_test = {"services_groups": 1,  
                     "vertices": 5, 
                     "power": 1, 
                     "edges_per_vertex": 1, 
                     "zero_appeal": 10,
                     "dbs": {"sdb1": 0.8, "sdb2": 0.3}
                    }
```
* Then, you can run the python file `RunServiceMeshGen.py`:
```shell
python RunServiceMeshGen.py
```
* To save the file `servicemesh.json` just generated, type `y` when the python script asks you for it. Now, copy the file to the NFS shared folder path, previously defined:
```shell
cp servicemesh.json $NFS_SHARED_FOLDER/
```

## 2. Generate the work model of the MicroService
The second step goal is to create the work model for the MicroService application, 
you can assign which job a service must execute when called.

```shell
cd MicroServiceSimulator/WorkModelGenerator
```
* Similarly to step one, edit the input parameters at the beginning of the `RunWorkModelGen.py` file.
Be careful to set the correct path to the `servicemesh.json` file saved in step one. If you want to include your own functions to the work model, check [here](CustomJobs.md).

```python
parameters = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [1, 250]}}
servicemesh_file_path = "../ServiceMeshGenerator/servicemesh.json"
```


* Run the python file `RunServiceMeshGen.py`:
```shell
python RunWorkModelGen.py
```

* We'll copy the `workmodel.json` file to the NFS folder on the next step, as it still needs to be edited by the `K8sYamlBuilder`.

## 3. Build yaml files for the Kubernetes deployment

As a result, the K8s Yaml Builder creates, on the `MicroServiceSimulator/Kubernetes/K8sYamlBuilder/yamls` path, one YAML per service with its `Deployment` and its relating `Service`, along with other files useful for the overall deployment of the MSS.

```shell
cd MicroServiceSimulator/Kubernetes/K8sYamlBuilder
```

* As always, edit the parameters in the `RunK8sYamlBuilder.py` file. You must edit the `nfs_conf` parameters with both the IP address and shared folder path of the NFS server.
  
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

* Run the python file `RunK8sYamlBuilder.py`:
```shell
python RunK8sYamlBuilder.py
```
* Copy the updated `workmodel.json` file in the NFS shared folder as follows:
```shell
cp workmodel.json $NFS_SHARED_FOLDER/
```

* Finally, if you want to deploy the just created yaml files to your K8s cluster, run:
```shell
kubectl apply -f yamls
```
