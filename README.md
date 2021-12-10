# **µBench** - A high customizable Microservice generator

**µBench** is a benchmarking tool for cloud/edge computing platforms that run microservice applications.
The tool creates *dummy* microservice applications that can be customized by the user to mimic the behavior of complex real-world microservice applications.

The user can model the topology of the application's service mesh, define the behaviors of the internal microservices using a portfolio of stress functions (e.g. for CPU, memory, I/O, network) or implementing new ones, choose HTTP or gRPC as the microservice protocol, etc.

After the microservice application is created, µBench deploys it on platforms for containerized applications, such as [Kubernetes](https://kubernetes.io). Developers of these platforms can test their innovations by observing related effects on µBench-created applications, which export per-microservice metrics, such as delay, load, etc.

µBench is targeted at researchers and developers of cloud platforms who cannot use real microservice applications to validate their results (e.g., new resource control mechanisms, AI-driven orchestration, etc.). At the same time, µBench can also be used for educational purposes to show students advantages and problems of microservice applications.

You can learn more about µBench [here](Docs/Manual.md)

This software is supported by:
- Liquid_Edge project, funded by Italian Ministry of University and Research within the PRIN 2017 program  
