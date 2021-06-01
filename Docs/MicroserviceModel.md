# Microservice Model

### Table of Content
* [Introduction](/README.md)
* [**Microservice Model**](/Docs/MicroserviceModel.md)
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
      * [K8s Yaml Builder](/Docs/Deployment.md#K8s-Yaml-Builder)
      * [K8s Deployer](/Docs/Deployment.md#K8s-Deployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Docs/Monitoring.md)
    * [Prometheus](/Docs/Monitoring.md#Prometheus)
    * [Grafana](/Docs/Monitoring.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
---

![service-cell-abstraction](service-cell-abstraction.png)

Using the **µBench** simulator a microservice application is composed of a collection of identical services which, at the time of their creation, only differ from their different ids, e.g. *s0, s1, s2... etc*.
The services are coupled to each other in a way that depends on the quello che gli hai detto, and all together make up the *service mesh*.

Each service becomes specialized in 



 appena creata la mesh. Dopo si specializzano leggendo da json, riconoscendosi da 

:
the underlying services are  

## Service Cell
Upon a service request, each service locally executes an **internal-service** and then carries out a set of calls towards **external-services**. An internal-service is a task that user can define as a python function to be inserted in the `/mnt/MSSharedData/JobFunctions` (see also [here](/Docs/MicroserviceModel.md#Custom-Functions)). However, each service has a pre-defined internal-service that is named `compute_pi`.

External services are grouped into a configurable number of groups (`service_groups`). Services from different groups are called in parallel; services from the same group are called sequentially. To mimic random paths on the service mesh, not all external services of a `service_group` are called, but only a subset of them, whose number is `seq_len` and these are chosen randomly (uniform distribution) from those in the `service_group`. 

---
## Internal Service

---
## External Services

---
## Docker Build

---
## Custom Functions

Each service of the microservice mesh executes an internal-service when called and by default it uses the `compute_pi` function. 
The default function keeps the CPU busy depending on the specified complexity of operations.

To try other scenarios, you can use your own specific functions to stress the aspect you whish to simulate: CPU, memory or storage. 
In order to do so, you must write your own python function and save it to the subfolder `InternalServiceFunctions` inside your NFS shared directory.
If you followed our [NFS configuration](/Docs/NFSConfig.md), create the subfolder into `/mnt/MSSharedData` using 
`mkdir /mnt/MSSharedData/InternalServiceFunctions`, otherwise create it according to your NFS configurations.

### How to write your own custom job

- As input, your function receives a dictionary with the parameters specified in the [work model generator](/WorkModelGenerator/README.md).
- As output, your function must return a string used as body for the response given back by a service.

> Note: each custom function must have a unique name, otherwise conflicts will occur.
Also, you can specify more than one custom function inside the same python file.

```python
def custom_function(params):
    
    ## your code here

    ## the response of the function must be a string
    response_body = "the body must be a string"

    return response_body
```
