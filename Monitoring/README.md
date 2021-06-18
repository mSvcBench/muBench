# Monitoring

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
* [**Monitoring**](/Monitoring/README.md#Monitoring)
    * [Prometheus](/Monitoring/README.md#Prometheus)
    * [Grafana](/Monitoring/README.md#Grafana)
* [Getting Started](/Docs/GettingStarted.md#Getting-Started)
    * [Example](/Docs/GettingStarted.md#Example) - A step by step walkthrough
    * [K8s Autopilot](/Docs/GettingStarted.md#K8s-Autopilot) - The lazy shortcut
---

With the following steps you will deploy on your Kubernetes environment: [Prometheus](https://prometheus.io/), [Prometheus Adapter](https://github.com/kubernetes-sigs/prometheus-adapter) and [Grafana](https://grafana.com/)

---
## Prometheus
First, create a new namespace called `monitoring` where we will deploy all the monitoring resources.

Prometheus will be available at: `http://<gateway-ip>:30000` after the successful deployment of the following commands:

```bash
kubectl create namespace monitoring
kubectl apply -f kubernetes-prometheus/
```
---
## Prometheus Adapter

Prometheus Adapter is suitable for use with the [Kubernetes Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
It can also replace the metrics server on clusters that already run Prometheus and collect the appropriate metrics.

You can install it using [Helm](https://helm.sh/docs/intro/install/).
We'll use the `prometheus-adapter-values.yaml` file for defining the µBench custom metrics to analyze.


```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install --namespace monitoring -f kubernetes-prometheus-adapter/prometheus-adapter-values.yaml prometheus-adapter prometheus-community/prometheus-adapter

# to check the status of the release
$ helm status prometheus-adapter --namespace monitoring
```

---
## Grafana
Finally, deploy Grafana to view the metrics through beautiful, flexible dashboards.

Grafana will be available at: `http://<gateway-ip>:30001`.

```bash
kubectl apply -f kubernetes-prometheus/
```