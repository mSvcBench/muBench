# **µBench** - A factory of benchmarking microservices applications


![service-cell-rest-grpc](Docs/microservices-rest-grpc.png)

**µBench** is a tool for benchmarking cloud/edge computing platforms that run microservice applications.
The tool creates *dummy* microservice applications that can be customized by the user and run on [Kubernetes](https://kubernetes.io) (and more).

µBench targets researchers and cloud platform developers who lack real microservice applications to benchmark their findings (e.g., new resource control mechanisms, AI-driven orchestration, etc.). Indeed, µBench can create these applications for them. At the same time, µBench can also be used for educational purposes to show advantages and problems of microservice applications to students.

µBench allows users control some properties of the microservice application it creates, such as: the topology of the service mesh, the behaviors of composing microservices using a portfolio of stress functions (e.g. for CPU, memory, I/O, network) or implementing new ones, the microservice-to-microservice API (HTTP or gRPC), etc. 

After the microservice application is created, µBench is able to run it on a Kubernetes cluster; however, the µBench architecture is open to include other container execution platforms as well. Developers of these platforms can test their innovations by observing related effects on µBench-created applications, which export per-microservice metrics, such as delay, load, throughput, etc.

You can learn more about µBench [here](Docs/Manual.md).

This software is supported by:
- Liquid_Edge project, funded by Italian Ministry of University and Research within the PRIN 2017 program.
## Quick Start
For a complete install guide, head over to the documentation [here](Docs/Manual.md#installation-and-getting-started). Instead, for a quick hands-on with **µBench** the following commands will deploy a microservice application composed of 20 services interconnected as the following [service mesh](examples/servicemeshC.png) to your Kubernetes cluster (this guide is intended for Debian-based distributions). You can find more information on the application to be deployed [here](examples/README.md).

```bash
# Create a virtual environment
$ python3 -m venv .venv
$ source .venv/bin/activate

# Install the requirements
$ sudo apt-get install build-essential libffi-dev libcairo2 -y
$ pip3 install -r requirements.txt

# NOTE: edit Configs/K8sParameters.json if your Kubernetes dns-resolver is different from kube-dns
$ python3 Deployers/K8sDeployer/RunK8sDeployer.py -c Configs/K8sParameters.json

# Check the correct deployment of the application 
$ kubectl get pods 
NAME                        READY   STATUS    RESTARTS   AGE
gw-nginx-74f8d64f56-zdcb4   1/1     Running   0          2m21s
s0-7548755f4d-7fl88         1/1     Running   0          2m18s
s1-b6785b88c-kg5fv          1/1     Running   0          2m18s
...
s19-77f98db56-cmvk5         1/1     Running   0          2m18s

# Test the correct execution of the application with 
$ curl http://<master-node-ip>:31113/s0
```

  
