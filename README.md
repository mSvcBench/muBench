# **µBench** - A factory of benchmarking microservices applications


![service-cell-rest-grpc](Docs/microservices-rest-grpc.png)

**µBench** is a tool for benchmarking cloud/edge computing platforms that run microservice applications.
The tool creates *dummy* microservice applications that can be customized by the user and run on [Kubernetes](https://kubernetes.io).

µBench targets researchers and cloud platform developers who lack real microservice applications to benchmark their findings (e.g., new resource control mechanisms, AI-driven orchestration, etc.). Indeed, µBench can create these applications for them. At the same time, µBench can also be used for educational purposes to show advantages and problems of microservice applications to students.

µBench allows users control some properties of the microservice application it creates, such as: - the topology of the service mesh 
- the behaviors of composing microservices using a portfolio of stress functions (e.g. for CPU, memory, I/O, network) or implementing new ones, 
- the microservice-to-microservice API (HTTP or gRPC)
- the CPU and Memory resources assigned to microservices and their number of replicas  

µBench provides a comprehensive monitoring framework consisting of Prometheus, Grafana, Istio, and Jaeger through which to observe the performance of the produced benchmark applications.

<p align="center">
<img width="100%" src="Monitoring/kubernetes-prometheus-operator/muBenchMonitors.png">
</p>

##µBench Manual
You can learn how to use µBench to create and monitor your application by reading the **[µBench manual](Docs/Manual.md)**.


  
## Quick Start
For a complete install guide, head over to the [manual](Docs/Manual.md#installation-and-getting-started). Instead, for a quick hands-on with µBench the following commands will deploy a microservice application composed of 10 services with a star topology service mesh. Clients send requests to s0 and s0 sequentially calls all other services before sending the result to clients. Each service equally stresses the CPU. 

We assume that on your host, you have Docker and have access to a Kubernetes cluster with `kubectl` tool. If you need to configure a Kubernetes cluster (e.g., with Minikube) or for other configurations read the [manual](Docs/Manual.md#installation-and-getting-started).

We will use the Docker µBench container that contains all the necessary software.

Run the µBench container
```zsh
docker run -d --name mubench msvcbench/mubench
```

Copy the `.kube/config ` file you use in your host to access the Kubernetes cluster in the container
```zsh
kubectl config view --flatten > config
docker cp config mubench:/root/.kube/config
```

Verify that µBench container can access your cluster, e.g., by using next command from your host
```zsh
docker exec mubench kubectl get nodes
``` 

Enter the µBench container with:
```zsh
docker exec -it mubench bash
``` 

Now your terminal should be in the µBench container from which you will run next commands
```zsh

╱╱╱╭━━╮╱╱╱╱╱╱╱╱╱╭╮
╱╱╱┃╭╮┃╱╱╱╱╱╱╱╱╱┃┃
╭╮╭┫╰╯╰┳━━┳━╮╭━━┫╰━╮
┃╰╯┃╭━╮┃┃━┫╭╮┫╭━┫╭╮┃
┃┃┃┃╰━╯┃┃━┫┃┃┃╰━┫┃┃┃
╰┻┻┻━━━┻━━┻╯╰┻━━┻╯╰╯

root@64ae03d1e5b8:~# 
``` 

Deploy the µBench demo app with
```zsh
cd $HOME/muBench
python3 Deployers/K8sDeployer/RunK8sDeployer.py -c Configs/K8sParameters.json
``` 

Check the correct deployment of the application pods with  
```zsh
kubectl get pods 
```
You should see the following pods
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

Test the correct execution of the application with 
```zsh
curl http://<MASTER_IP>:31113/s0
```
where `MASTER_IP` is the IP address of the master-node of the Kubernetes cluster.
If you receive back a sequence of random letters, it means that your first µBench app is running :-). 

Read the [manual](Docs/Manual.md) to create and monitor your benchmark apps.
  
> **_NOTE:_**: edit Configs/K8sParameters.json if your Kubernetes dns-resolver is different from kube-dns

##Cite Us
The description of µBench and some use-cases has been published in IEEE Transactions on Parallel and Distributed Systems. If you use the µBench please cite the following publication:

>A. Detti, L. Funari, L. Petrucci, "µBench: an open-source factory of benchmark microservice applications", IEEE Transactions on Parallel and Distributed Systems

To reproduce the tests of the paper read [here](Docs/reproducibility.md)



## Acknowledge
This software is supported by:
- Liquid_Edge project, funded by Italian Ministry of University and Research within the PRIN 2017 program.
- Italian PNRR Restart Program