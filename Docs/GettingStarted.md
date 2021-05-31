# Getting Started

### Table of Content
* [Introduction](/README.md)
* [Microservice Model](/Docs/MicroserviceModel.md)
  * [Service Cell](/Docs/MicroserviceModel.md#Service-Cell)
  * [Internal Service](/Docs/MicroserviceModel.md#Internal-Service)
  * [External Services](/Docs/MicroserviceModel.md#External-Services)
  * [Docker Build](/Docs/MicroserviceModel.md#Docker-Build)
  * [Custom Functions](/Docs/MicroserviceModel.md#Custom-Functions)
* [Building Tools](/Docs/BuildingTools.md)
  * [Service Mesh Generator](/Docs/BuildingTools.md#Service-Mesh-Generator)
  * [Work Model Generator](/Docs/BuildingTools.md#Work-Model-Generator)
  * [Workload Generator](/Docs/BuildingTools.md#Workload-Generator)
  * [Runner](/Docs/BuildingTools.md#Runner)
* [Deployment](/Docs/Deployment.md)
    * [Kubernetes](/Docs/Deployment.md#Kubernetes)
      * [K8s Yaml Builder](/Docs/Deployment.md#K8sYamlBuilder)
      * [K8s Deployer](/Docs/Deployment.md#Kubernetes#K8sDeployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Docs/Monitoring.md)
    * [Prometheus](/Docs/Monitoring.md#Prometheus)
    * [Grafana](/Docs/Monitoring.md#Grafana)
* [**Getting Started**](/Docs/GettingStarted.md)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#AutoPilot) - The lazy shortcut
---

## Example
### A step by step walkthrough
### Configure MicroServiceSimulator from scratch

In this file we describe the necessary step to run the MicroService Simulator from scratch.
If you leave the files unchanged, it will generate a Microservice composed of 5 services.

Before we begin, export the path to your NFS shared folder as an environment variable.
```shell
export NFS_SHARED_FOLDER="/mnt/MSSharedData" 
```

### Step 1: Generate the service mesh of the MicroService Application
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

### Step 2: Generate the work model of the MicroService Application
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
python3 RunWorkModelGen.py
```

* We'll copy the `workmodel.json` file to the NFS folder on the next step, as it still needs to be edited by the `K8sYamlBuilder`.

### Step 3: Build yaml files for the Kubernetes deployment

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
python3 RunK8sYamlBuilder.py
```

* Copy the updated `workmodel.json` file in the NFS shared folder as follows:

```shell
cp workmodel.json $NFS_SHARED_FOLDER/
```

* Finally, if you want to deploy the just created yaml files to your K8s cluster, run:

```shell
kubectl apply -f yamls
```

---
## Autopilot
### The lazy shortcut

The autopilot is an easy way to deploy all the component of the MicroServiceSimulator. It's work under two assumptions:
* Run the autopilot script on the K8s Master Node
* The [NFS server](/Docs/NFSConfig.md) must have been configured on the same K8s Master Node

### Run AutoPilot
Before running the script edit the configuration file `AutoPilotConf.py`. This file contains the configurations of all other modules seen in the [example](/Docs/Example.md).  

* The only parameter that you must edit in this file is `nfs_conf` parameters with both the IP address and shared folder path of the NFS server.

```python
nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}
```

* Then, you can run the `AutoPilot.py` script:

```shell
python3 AutoPilot.py
```

* add workflow drawio:
 
TODO

    * Properly edit the AutoPilotConf file
    * Run autopilot, it check if there is a deployment yet. 
      * Yes -> asks for undeploy, if yes delete the deployment and remove yaml files
      * No -> Generate yaml files and deploy
        
    * Asks to generate the workload file
    * DONE! :)
