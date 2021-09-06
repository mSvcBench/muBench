# Getting Started

### Table of Content
* [Introduction](/README.md)
* [Microservice Model](/Docs/MicroserviceModel.md#Microservice-Model)
  * [Service Cell](/Docs/MicroserviceModel.md#Service-Cell)
  * [Internal Service](/Docs/MicroserviceModel.md#Internal-Service)
  * [External Services](/Docs/MicroserviceModel.md#External-Services)
  * [Custom Functions](/Docs/MicroserviceModel.md#Custom-Functions)
* [Building Tools](/Docs/BuildingTools.md#Building-Tools)
  * [Service Mesh Generator](/Docs/BuildingTools.md#Service-Mesh-Generator)
  * [Work Model Generator](/Docs/BuildingTools.md#Work-Model-Generator)
  * [Workload Generator](/Docs/BuildingTools.md#WorkLoad-Generator)
  * [Runner](/Docs/BuildingTools.md#Runner)
* [Deployment](/Docs/Deployment.md#Deployment)
    * [Kubernetes](/Docs/Deployment.md#Kubernetes)
      * [K8s Yaml Builder](/Docs/Deployment.md#K8s-Yaml-Builder)
      * [K8s Deployer](/Docs/Deployment.md#K8s-Deployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Monitoring/README.md#Monitoring)
    * [Prometheus](/Monitoring/README.md#Prometheus)
    * [Grafana](/Monitoring/README.md#Grafana)
* [**Getting Started**](/Docs/GettingStarted.md#Getting-Started)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
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

If you want to tune the parameters for the generation of the service mesh, edit the input parameters in `ServiceMeshParameters.json` as advised [here](/ServiceMeshGenerator/README.md#Input-Parameters) . 

```json
{
   "ServiceMeshParameters": {
      "vertices": 10,
      "external_service_groups": 10,
      "power": 100,
      "seq_len": 100,
      "zero_appeal": 0.01,
      "dbs": {
         "nodb": 1.0,
         "sdb1": 0.0,
         "sdb2": 0.0
      }
   },
   "OutputPath": "../SimulationWorkspace"
}
```

Then, you can run the python file `RunServiceMeshGen.py`:

```shell
python3 RunServiceMeshGen.py
```

Now, copy the files `servicemesh.json` and `servicemesh.png` from the `OutputPath` specified in the JSON file, to the NFS shared folder path, previously defined:

```shell
cd ../SimulationWorkspace
cp servicemesh.json $NFS_SHARED_FOLDER/
cp servicemesh.png $NFS_SHARED_FOLDER/
```

### Step 2: Generate the work model of the MicroService Application
The second step is about creating the work model for the MicroService application, 
you can assign which job a service must execute when called.

```shell
cd MicroServiceSimulator/WorkModelGenerator
```

Similarly to step one, edit the input parameters in `WorkModelParameters.json` as advised [here](/WorkModelGenerator/README.md#Input-Parameters). 
If you want to include your own functions to the work model, check [here](CustomJobs.md).

> Be careful to set the correct path to the `servicemesh.json` file saved in step one, using `ServiceMeshFilePath`. 

```json
{
   "WorkModelParameters":{
      "compute_pi":{
         "probability":0.3,
         "mean_bandwidth":11,
         "range_complexity":[101, 101]
      },
      "colosseum": {
         "probability": 0.6
      },
      "databases_function": {
         "type": "database",
         "probability": 0.6
      },
      "request_method": "gRPC",
      "databases_prefix": "sdb"
   },
   "ServiceMeshFilePath": "../SimulationWorkspace/servicemesh.json",
   "OutputPath": "../SimulationWorkspace"
}
```

Then, you can run the python file `RunWorkModelGen.py` file.

```shell
python3 RunWorkModelGen.py
```

On the next step, we'll copy the `workmodel.json` file, from the `OutputPath` specified in the JSON file, to the NFS folder, as it needed for the `K8sYamlBuilder`.

```shell
cd ../SimulationWorkspace
cp workmodel.json $NFS_SHARED_FOLDER/
```

### Step 3: Build yaml files for the Kubernetes deployment

The K8s Yaml Builder creates and saves to the `<OutputPath>/yamls` path, one YAML per service with its `Deployment` and its relating `Service`, along with other files useful for the overall deployment of the Microservice Application.

```shell
cd MicroServiceSimulator/Kubernetes/K8sYamlBuilder
```
  
As always, edit the input parameters in `K8sParameters.json` as advised [here](/Docs/Deployment.md#Input-Parameters). 

```json
{
   "K8sParameters": {
      "prefix_yaml_file":"MicroServiceDeployment",
      "namespace": "default",
      "image": "lucapetrucci/microservice_v2:latest",
      "cluster_domain": "cluster",
      "path": "/api/v1"
   },
   "NFSConfigurations": {
      "address": "10.3.0.4",
      "mount_path": "/mnt/MSSharedData"
   },
   "WorkModelPath": "../../SimulationWorkspace/workmodel.json",
   "OutputPath": "../../SimulationWorkspace"
}
```

Then, run the python file `RunK8sYamlBuilder.py`:

```shell
python3 RunK8sYamlBuilder.py
```

Copy the updated `workmodel.json` from the `OutputPath` specified in the JSON file, to the NFS shared folder as follows:

```shell
cd ../../SimulationWorkspace
cp workmodel.json $NFS_SHARED_FOLDER/
```

Finally, if you want to deploy the just created yaml files to your K8s cluster, run:

```shell
kubectl apply -f yamls
```

Now, head over to the [Runner](/Docs/BuildingTools.md#Runner) to start the simulations.

---
## K8s Autopilot
### The lazy shortcut

The K8s autopilot is an easy way to deploy all the component of the **µBench** tool. 
To sum up, the autopilot will:
* use the Service Mesh Generator to generate the `servicemesh.json`
* use the Work Model Generator to generate the `workmodel.json`
* use the K8s Yaml Builder to generate the YAML files
* deploy all the Kubernetes objects to your K8s cluster. 

It works under two assumptions:
* Run the K8s autopilot script on the K8s Master Node
* The [NFS server](/Docs/NFSConfig.md) must have been configured on the same K8s Master Node

### Run K8s Autopilot
Before running the script edit the configuration file `K8sAutopilotConf.json`. This file contains the configurations of all other modules seen in the [example](/Docs/GettingStarted.md#Example) above.  

```shell
cd MicroServiceSimulator/Kubernetes/K8sAutopilot
```

> Remember to edit the `NFSConfigurations` parameters with both the IP address and shared folder path of the NFS server.

Then, you can run the `K8sAutopilot.py` script:

```shell
python3 K8sAutopilot.py
```

Finally, run the `K8sAutopilot.py` script.
You can specify your custom configuration file as argument otherwise, if you do not indicate any argument, it will use the default configuration file (`K8sAutopilotConf.json`) located inside its directory:

```zsh
python3 K8sAutopilot.py [PARAMETER_FILE]
```
