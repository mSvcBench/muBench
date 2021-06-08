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

In this section, we'll describe how to create and deploy the *µBench* objects to a Kubernetes environment.

Once you have (i), defined your service mesh topology with the [Service Mesh Generator](/ServiceMeshGenerator/README.md#Service-Mesh-Generator), (ii), described the behavior of each service when reached using the [Work Model Generator](/WorkModelGenerator/README.md#Work-Model-Generator) and (iii), generated the load of the simulation with the [WorkLoad Generator](/WorkLoadGenerator/README.md#Workload-Generator) you are ready to deploy the service mesh on Kubernetes.

We'll use the [K8s Yaml Builder](/Docs/Deployment.md#K8sYamlBuilder) to translate the `workmodel` into K8s deployable objects.


### K8s Yaml Builder
The `K8sYamlBuilder` leverages the `workmodel.json` file to build valid YAML files, used to deploy the objects to the Kubernetes environment.

In particular, it will create the following objects:
* A `PersistentVolume` along with a `PersistentVolumeClaim` to make the [NFS shared directory](/Docs/NFSConfig.md) visible as a volume for each pod, containing the shared configuration files, ;
* The gateway of the microservice application as a `Deployment`, reachable from outside the cluster thanks to its related `NodePort` service;
* The configuration of the Nginx gateway through a `ConfigMap`;
* Each service of the service mesh as a `Deployment` associated to its `NodePort` service.

## Input Parameters
As input, the K8s Yaml Builder needs some information related to the pods, such as the the Docker `image`, the `namespace` of the deployment, as well as the K8s `cluster_domain` and the `path` which, together with its [FQDN](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/), it will use it to wait for incoming requests.
For example, a deployment of a µBench service called `s0` that uses the parameters of the example, will be listening at `http://s0.default.svc.cluster.local/api/v1`.

```json
{
   "K8sParameters": {
      "prefix_yaml_file":"MicroServiceDeployment",
      "namespace": "default",
      "image": "lucapetrucci/microservice:latest",
      "cluster_domain": "cluster",
      "path": "/api/v1"
   },
   "NFSConfigurations": {
      "address": "192.168.0.44",
      "mount_path": "/mnt/MSSharedData"
   },
   "WorkModelPath": "../../SimulationWorkspace/workmodel.json",
   "OutputPath": "../../SimulationWorkspace"
}
```

linked to 

the service will listen to:
in this way, a service will be reached through its [FQDN](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) 



the information related to the 

## Output Understanding
## Run the script
Edit the `WorkLoadParameters.json` file before running the `WorkLoadGenerator`.

Finally, run the script to obtain and save to the `OutputPath` the `workload.json` as follows:
```
python3 RunWorkModelGen.py
```


and the following input parameters into K8s deployable YAML files:

```json
{
   "K8sParameters": {
      "prefix_yaml_file":"MicroServiceDeployment",
      "namespace": "default",
      "image": "lucapetrucci/microservice:latest",
      "cluster_domain": "cluster",
      "path": "/api/v1"
   },
   "NFSConfigurations": {
      "address": "192.168.0.144",
      "mount_path": "/kubedata/MSSharedData"
   },
   "WorkModelPath": "../../SimulationWorkspace/workmodel.json",
   "OutputPath": "../../SimulationWorkspace"
}
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

Up until to now, the deploying part of the MSS requires Kubernetes, but the availability can be expanded in the future. 

TODO