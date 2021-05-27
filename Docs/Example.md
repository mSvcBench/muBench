# Configure MicroServiceSimulator from scratch

In this file we describe the necessary step to run the MicroService Simulator from scratch.
If you leave the files unchanged, it will generate a Microservice composed of 5 services.

Before we begin, export the path to your NFS shared folder as an environment variable.
```shell
export NFS_SHARED_FOLDER="/mnt/MSSharedData" 
```

## 1. Generate the service mesh of the MicroService Application
We start with the generation of the service mesh that eventually produces two files `servicemesh.json` and `servicemesh.png`. The .png is a picture of the generated mesh. Service mesh detail can be seen [here](../ServiceMeshGenerator/README.md)

```shell
cd MicroServiceSimulator/ServiceMeshGenerator
```
* If you want to tune the parameters for the generation of the service mesh, edit the input parameters in `ServiceMeshParameters.json`.

* Then, you can run the python file `RunServiceMeshGen.py`:
```shell
python3 RunServiceMeshGen.py
```
* Now, copy the files `servicemesh.json` and `servicemesh.png` to the NFS shared folder path, previously defined:
```shell
cp servicemesh.json $NFS_SHARED_FOLDER/
cp servicemesh.png $NFS_SHARED_FOLDER/
```

## 2. Generate the work model of the MicroService Application
The second step is about creating the work model for the MicroService application, 
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
