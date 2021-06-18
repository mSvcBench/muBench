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
* [Monitoring](/Docs/Monitoring/README.md#Monitoring)
    * [Prometheus](/Docs/Monitoring/README.md#Prometheus)
    * [Grafana](/Docs/Monitoring/README.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md#Getting-Started)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
---

## Kubernetes

In this section, we'll describe how to create and deploy the *µBench* objects to a Kubernetes environment.

Once you have (i), defined your service mesh topology with the [Service Mesh Generator](/ServiceMeshGenerator/README.md#Service-Mesh-Generator), (ii), described the behavior of each service using the [Work Model Generator](/WorkModelGenerator/README.md#Work-Model-Generator) and (iii), generated the simulation load with the [WorkLoad Generator](/WorkLoadGenerator/README.md#Workload-Generator) you are ready to deploy the service mesh on Kubernetes.

We'll use the [K8s Yaml Builder](/Docs/Deployment.md#K8sYamlBuilder) to translate the `workmodel` into K8s deployable objects.


### K8s Yaml Builder
The `K8sYamlBuilder` leverages the `workmodel.json` file to build valid YAML files, used to deploy the objects to the Kubernetes environment.

In particular, it will create the following objects:
* A `PersistentVolume` with its `PersistentVolumeClaim` to make the [NFS shared directory](/Docs/NFSConfig.md) visible as a volume for each pod, as it contains the configuration files;
* The NGINX gateway of the microservice application as a `Deployment`, reachable from the outside of the cluster thanks to its related `NodePort` service;
* The configuration of the NGINX gateway through a `ConfigMap`;
* Each service of the service mesh as a `Deployment`.

## Input Parameters
As input, the K8s Yaml Builder needs some information related to your environment, such as the the Docker `image`, the `namespace` of the deployment, as well as the K8s `cluster_domain` and the `path`, which, together with its [FQDN](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/), the service container inside each pod will use it to listen for incoming requests.
For example, a deployment of a µBench service called `s0` that uses the parameters of the example, will be listening at `http://s0.default.svc.cluster.local/api/v1`.

You can change the name of the output YAML files of the services of the microservice application by specifying the `prefix_yaml_file`.

Also, you need to define the IP address of the NFS servers with `address`, in our case it was deployed on the K8s master node, and the path of the directory it shares with the `mount_path`. 

The K8sYamlBuilder will use as input the `workmodel.json` specified by the `WorkModelPath` and will generate all the YAML files into the `yamls` directory inside the `OutputPath`.

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

## Output Understanding

Using the example above, the K8sYamlBuilder will generate the following files:

```bash
ls SimulationWorkspace/yamls
PersistentVolumeMicroService.yaml
DeploymentNginxGw.yaml
ConfigMapNginxGw.yaml
MicroServiceDeployment-s0.yaml
MicroServiceDeployment-s1.yaml
MicroServiceDeployment-s2.yaml
...
```

## Run the script
Edit the `WorkLoadParameters.json` file before running the `WorkLoadGenerator`.

Finally, run the script to obtain all the YAML files inside the `SimulationWorkspace/yamls`directory as follows:

```
python3 RunWorkModelGen.py
```

### K8s Deployer

---
## Further Works

Up to now, the µBench simulator works in a Kubernetes environment.
We plan to extend its availability on [Docker Swarm](https://docs.docker.com/get-started/swarm-deploy/#prerequisites) in the near future.