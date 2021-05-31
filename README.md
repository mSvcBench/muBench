# **µBench** - A high customizable Microservice simulator

**µBench** is a high customizable simulator of microservice applications.
This project aims at facilitating the process of modeling, deploying and monitoring, to reproduce the behavior of complex applications. 

You can shape the mesh topology of interconnected services that describes a microservice application.
You can define the behaviors of the application 
thanks to the ability of implementing your own stress functions which gives you total control on the aspect to stress, e.g. the CPU, memory, I/O, network, etc.

To simulate real case scenarios, **µBench** deploys the modeled applications on top of distributed environments, like [Kubernetes](https://kubernetes.io).

In this repository, you can learn more about [how µBench abstracts](/Docs/MicroserviceModel.md) the workflow of the microservice applications, [the architecture](/Docs/BuildingTools.md) of µBench and a [step by step example](/Docs/Example.md) that walk you through the potentialities of µBench.
Also, you can use the [Autopilot](/Docs/AutoPilot.md) to perform the [example](/Docs/Example.md) steps automatically.

---
### Table of Content
* [**Introduction**](/README.md)
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
      * [K8s Yaml Builder](/Docs/Deployment.md#K8s-Yaml-Builder)
      * [K8s Deployer](/Docs/Deployment.md#K8s-Deployer)
    * [Further Works](/Docs/Deployment.md#Further-Works)
* [Monitoring](/Docs/Monitoring.md)
    * [Prometheus](/Docs/Monitoring.md#Prometheus)
    * [Grafana](/Docs/Monitoring.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#AutoPilot) - The lazy shortcut
