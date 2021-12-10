# **µBench** - A high customizable Microservice generator

**µBench** is a benchmarking tool for cloud/edge computing platforms aimed at running microservice applications.
The tool creates *dummy* microservice applications that can be customized by the user to mimic the behavior of complex real-world microservice applications.

The user can model the topology of the application's service mesh, define the behaviors of the internal microservices using a portfolio of stress functions (e.g. for CPU, memory, I/O, network) or implementing new ones, choose HTTP or gRPC as the microservice protocol, etc.

After the microservice application is created, µBench deploys it on platforms for containerized applications, such as [Kubernetes](https://kubernetes.io). Developers of these platforms can test their innovations by observing their effect on µBench-created applications, which export per-microservice metrics, such as delay, load, etc., through a Prometheus server. 

You can learn more about µBench [here](Docs/Manual.md)

This software is supported by:
- Liquid_Edge project, funded by Italian Ministry of University and Research within the PRIN 2017 program  
