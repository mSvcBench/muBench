# **µBench** - A high customizable Microservice simulator

**µBench** is a high customizable simulator of microservice applications.
This project aims at facilitating the process of modeling, deploying and monitoring, to reproduce the behavior of complex applications. 

You can shape the mesh topology of interconnected services that describes a microservice application.
You can define the behaviors of the application thanks to the ability of implementing your own stress functions which gives you total control on the aspect to stress, e.g. the CPU, memory, I/O, network, etc.

To simulate real case scenarios, **µBench** deploys the modeled applications on top of distributed environments, like [Kubernetes](https://kubernetes.io).

In this repository, you can learn more about [how µBench abstracts](/Docs/MicroserviceModel.md#Microservice-Model) the workflow of the microservice applications, [the architecture](/Docs/BuildingTools.md#Building-Tools) of µBench and a [step by step example](/Docs/GettingStarted.md#Example) that walk you through the potentialities of µBench.
Also, you can use the [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) to perform all the steps of the [example](/Docs/GettingStarted.md#Example) automatically up to the deployment of the microservice to your Kubernetes cluster.

---
### Table of Content
* [**Introduction**](/README.md)
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
