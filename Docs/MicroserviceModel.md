# Microservice Model

### Table of Content
* [Introduction](/README.md)
* [**Microservice Model**](/Docs/MicroserviceModel.md#Microservice-Model)
  * [Service Cell](/Docs/MicroserviceModel.md#Service-Cell)
  * [Internal Service](/Docs/MicroserviceModel.md#Internal-Service)
  * [External Services](/Docs/MicroserviceModel.md#External-Services)
  * [Custom Functions](/Docs/MicroserviceModel.md#Custom-Functions)
* [Building Tools](/Docs/BuildingTools.md#Building-Tools)
  * [Service Mesh Generator](/Docs/BuildingTools.md#Service-Mesh-Generator)
  * [Work Model Generator](/Docs/BuildingTools.md#Work-Model-Generator)
  * [Workload Generator](/Docs/BuildingTools.md#Workload-Generator)
  * [Runner](/Docs/BuildingTools.md#Runner)
* [Deployment](/Docs/Deployment.md#Deployment)
    * [Kubernetes](/Docs/Deployment.md#Kubernetes)
      * [K8s Yaml Builder](/Docs/Deployment.md#K8s-Yaml-Builder)
      * [K8s Deployer](/Docs/Deployment.md#K8s-Deployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Docs/Monitoring/README.md#Monitoring)
    * [Prometheus](/Docs/Monitoring/README.md#Prometheus)
    * [Grafana](/Docs/Monitoring/README.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md#Getting-Started)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
---

![service-cell-abstraction](service-cell-abstraction.png)

## Service Cell

A microservice application is made up as a collection of loosely coupled identical services which, at the time of their creation, only differ from their different IDs, e.g. *s0, s1, s2... etc*.
The services are interconnected to each other depending on the configuration parameters and their combinations compose the *service mesh*.

We'll use the analogy of the cell and its DNA.
Almost every cell in a person’s body has *the same DNA*.
Although having the same DNA, each cell becomes specialized in order to perform different functions.  

With this in mind, we thought of a service like a cell, since it is the building block of a microservice application.
Every service share two common files: the `servicemesh.json` and the `workmodel.json` that, as the DNA of a cell, contain all the information needed for the service to stand out from the others and shape the application.

All the services are [Docker containers](https://www.docker.com/resources/what-container) that use the same image.
Only when created each service learns, from the `servicemesh.json` file, which services it is connected to (*external-services*) and, from the `workmodel.json`, all the useful information for being fully functionable inside the application, like the function they must perform (*internal-service*) and the url used to listen to requests of connected services.
Upon a service request, each service locally executes an *internal-service* and then carries out a set of calls towards *external-services*.
Visit [this section](/MicroServiceCellAbstraction/README.md) if you want to build your own version of the Docker image each service use.

---
## Internal Service
An internal-service is a task that users can define as a python function to be inserted in the [shared folder](/Docs/NFSConfig.md) `/mnt/MSSharedData/JobFunctions` (see also **custom functions** below for details). However, each service has a default internal-service that is named `compute_pi`.

### Custom Functions
Each service of the microservice mesh executes an internal-service when called and by default it uses the `compute_pi` function. 
The default function keeps the CPU busy depending on the specified complexity of operations.

To try other scenarios, you can use your own specific functions to stress the aspect you whish to simulate: CPU, memory or storage. 
In order to do so, you must write your own python function and save it to the subfolder `InternalServiceFunctions` inside your NFS shared directory.
If you followed our [NFS configuration](/Docs/NFSConfig.md), create the subfolder into `/mnt/MSSharedData` using 
`mkdir /mnt/MSSharedData/InternalServiceFunctions`, otherwise create it according to your NFS configurations.

---
## External Services
External-services are grouped into a configurable number of groups (`service_groups`). Services from different groups are called in parallel; services from the same group are called sequentially. To mimic random paths on the service mesh, not all external services of a `service_group` are called, but only a subset of them, whose number is `seq_len` and these are chosen randomly (uniform distribution) from those in the `service_group`. 

External-services are grouped into a configurable number of groups (`service_groups`). Services from different groups are called in parallel; services from the same group are called sequentially. To mimic random paths on the service 
, not all external services of a `service_group` are called, but only a subset of them, whose number is `seq_len` and these are chosen randomly (uniform distribution) from those in the `service_group`. 

---
### How to write your own custom job

As **input**, your function receives a dictionary with the parameters specified in the [work model generator](/WorkModelGenerator/README.md).

As **output**, your function must return a string used as body for the response given back by a service.

> Note: each custom function must have a **unique name**, otherwise conflicts will occur.
Also, you can specify more than one custom function inside the same python file.

```python
def custom_function(params):
    
    ## your code here

    ## the response of the function must be a string
    response_body = "the body must be a string"

    return response_body
```
