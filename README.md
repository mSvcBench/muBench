# **µBench** - A Factory of Benchmarking Microservices Applications

![service-cell-rest-grpc](Docs/microservices-rest-grpc.png)

**µBench** is a tool designed for benchmarking cloud/edge computing platforms that run microservice applications. The tool generates *dummy* microservice applications, which can be customized by the user and deployed on [Kubernetes](https://kubernetes.io).

µBench is particularly useful for researchers and cloud platform developers who need real microservice applications to benchmark their findings, such as new resource control mechanisms or AI-driven orchestration. µBench can create these applications for them. Additionally, µBench can be used for educational purposes to demonstrate the advantages and challenges of microservice applications to students.

µBench allows users to control various properties of the microservice applications it creates, including:
- The dependency graph of the microservice application
- The behaviors of composing microservices using a portfolio of stress functions (e.g., for CPU, memory, I/O, network) or implementing new ones
- The microservice-to-microservice API (HTTP or gRPC)
- The CPU and Memory resources assigned to microservices and their number of replicas

µBench provides a comprehensive monitoring framework consisting of Prometheus, Grafana, Istio, Kiali, and Jaeger, through which you can observe the performance of the produced benchmark applications.

<p align="center">
<img width="100%" src="Monitoring/kubernetes-full-monitoring/muBenchMonitors.png">
</p>

A poster outlining the main features of µBench is available [here](Docs/mubench-poster.pdf).

## µBench Manual
You can learn how to use µBench to create and monitor your application by reading the **[µBench manual](Docs/Manual.md)**.

## Quick Start
For a complete installation guide, refer to the [manual](Docs/Manual.md#installation-and-getting-started). For a quick hands-on experience with µBench, the following commands will deploy a microservice application composed of 10 services with a star topology service graph. Clients send requests to `s0`, and `s0` sequentially calls all other services before sending the result to clients. Each service equally stresses the CPU.

We assume that you have Docker and access to a Kubernetes cluster with the `kubectl` tool configured (`.kube/config`). If you need to configure a Kubernetes cluster (e.g., with Minikube) or for other configurations, refer to the [manual](Docs/Manual.md#installation-and-getting-started).

We will use the Docker µBench container, which contains all the necessary software.

### Run the µBench Container
```zsh
docker run -it -id --name mubench -v ~/.kube/config:/root/.kube/config msvcbench/mubench
```

Update the `server` key of the `config` file with the correct IP address of the master node of the cluster, if necessary. Verify that the µBench container can access your cluster by using the following command from your host:
```zsh
docker exec mubench kubectl get nodes
```

### Enter the µBench Container
```zsh
docker exec -it mubench bash
```

Now your terminal should be in the µBench container from which you will run the next commands:
```zsh
╱╱╱╭━━╮╱╱╱╱╱╱╱╱╱╭╮
╱╱╱┃╭╮┃╱╱╱╱╱╱╱╱╱┃┃
╭╮╭┫╰╯╰┳━━┳━╮╭━━┫╰━╮
┃╰╯┃╭━╮┃┃━┫╭╮┫╭━┫╭╮┃
┃┃┃┃╰━╯┃┃━┫┃┃┃╰━┫┃┃┃
╰┻┻┻━━━┻━━┻╯╰┻━━┻╯╰╯

root@64ae03d1e5b8:~muBench#
```

### Deploy a µBench Example App
```zsh
cd $HOME/muBench
python3 Deployers/K8sDeployer/RunK8sDeployer.py -c Configs/K8sParameters.json
```

### Check the Deployment
```zsh
kubectl get pods
```
You should see the following pods:
```zsh
root@64ae03d1e5b8:~/muBench# k get pods
NAME                        READY   STATUS    RESTARTS   AGE
gw-nginx-5b66796c85-fpqvc   2/2     Running   0          11m
s0-7d7f8c875b-gk2pq         2/2     Running   0          11m
s1-8fcb67d75-pncwq          2/2     Running   0          11m
s2-558f544b94-kft64         2/2     Running   0          11m
s3-79485f9857-5j79h         2/2     Running   0          11m
s4-9b6f9f77b-dklvm          2/2     Running   0          11m
s5-6ccddd9b47-n5pz7         2/2     Running   0          11m
s6-7c87c79cd6-pt26s         2/2     Running   0          11m
s7-5fb7cbff7c-hkd6t         2/2     Running   0          11m
s8-5549949968-72q2z         2/2     Running   0          11m
s9-9576b784c-4npsj          2/2     Running   0          11m
```

### Test the Application
```zsh
curl http://<MASTER_IP>:31113/s0
```
where `MASTER_IP` is the IP address of the master node of the Kubernetes cluster. If you receive back a sequence of random letters, it means that your first µBench app is running successfully.

Read the [manual](Docs/Manual.md) to create and monitor your benchmark apps.

> **_NOTE:_**: Edit `Configs/K8sParameters.json` if your Kubernetes DNS resolver service is different from `kube-dns`. For instance, for some clusters, it is named `coredns`. Otherwise, the nginx pod will get an error status.

## Cite Us
The description of µBench and some use cases have been published in IEEE Transactions on Parallel and Distributed Systems. If you use µBench, please cite the following publication:

> A. Detti, L. Funari, and L. Petrucci, "μBench: An Open-Source Factory of Benchmark Microservice Applications," in IEEE Transactions on Parallel and Distributed Systems, vol. 34, no. 3, pp. 968-980, 1 March 2023, doi: 10.1109/TPDS.2023.3236447.

To reproduce the tests of the paper, read [here](Docs/reproducibility.md).

## Critical Changes from Previous Versions
> **ServiceMeshGenerator replaced by ServiceGraphGenerator**. In the previous version of µBench, we used the term *service mesh* to denote the dependency graph between microservices. In the current version, we have replaced this term with *service graph* since today the term service mesh denotes tools such as Istio. Therefore, many keyworks and file names are changed. For example, `ServiceMeshGenerator` is now `ServiceGraphGenerator`, `ServiceMeshParameters.json` is now `ServiceGraphParameters.json`, etc.

> **mean_bandwidth replaced by mean_response_size**. In the previous version of µBench, we used the JSON key `mean_bandwidth` to indicate the mean response size of `pi` and `loader` internal functions. Now the key has been changed to `mean_response_size`.

## Acknowledgments
This software is supported by:
- Liquid_Edge project, funded by the Italian Ministry of University and Research within the PRIN 2017 program.
- Italian PNRR Restart Program
