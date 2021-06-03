# Deployment

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
  * [Workload Generator](/Docs/BuildingTools.md#Workload-Generator)
  * [Runner](/Docs/BuildingTools.md#Runner)
* [**Deployment**](/Docs/Deployment.md#Deployment)
    * [Kubernetes](/Docs/Deployment.md#Kubernetes)
      * [K8s Yaml Builder](/Docs/Deployment.md#K8sYamlBuilder)
      * [K8s Deployer](/Docs/Deployment.md#Kubernetes#K8sDeployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Docs/Monitoring.md#Monitoring)
    * [Prometheus](/Docs/Monitoring.md#Prometheus)
    * [Grafana](/Docs/Monitoring.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md#Getting-Started)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
---

## Kubernetes

TODO

Up until to now, the deploying part of the MSS requires Kubernetes, but the availability can be expanded in the future. 

### K8s Yaml Builder
The [K8sYamlBuilder](Kubernetes) comines the `servicemesh.json`, `workmodel.json` and the following input parameters into K8s deployable YAML files:

```shell
prefix_yaml_output_file = "MicroServiceDeployment"
deployment_namespace = "default"
image_name = "lucapetrucci/microservice:latest"
cluster_domain = "cluster"
service_path = "/api/v1"
var_to_be_replaced = {}  # (e.g {"{{string_in_template}}": "new_value", ...} )

nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}
```

Some changes to the configuration paramteres are mandatory, others optional.
In particular, it is necessary to update the fields regarding the K8s namespace, NFS server address as well as its mounted path, accordingly with your environment.
Concerning the other parameters, we highly suggest changing them only to expert users, since it would require further changes across the code, as well as the rebuilt of the Docker images each services make use of.

As a result, the K8s Yaml Builder creates, on the `Kubernetes/K8sYamlBuilder/yamls` path, one YAML per service with its `Deployment` and its relating `Service`, along with other files useful for the overall deployment of the MSS.

```zsh
host@hostname:~/MicroServiceSimulator/Kubernetes/K8sYamlBuilder/yamls$ ls
ConfigMapNginxGw.yaml
DeploymentNginxGw.yaml
MicroServiceDeployment-s0.yaml
MicroServiceDeployment-s1.yaml
MicroServiceDeployment-s2.yaml
MicroServiceDeployment-s3.yaml
MicroServiceDeployment-s4.yaml
PersistentVolumeMicroService.yaml
```

### K8s Deployer

---
## Further Works

TODO