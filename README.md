# **µBench** - A high customizable Microservice simulator


![service-cell-rest-grpc](Docs/microservices-rest-grpc.png)

**µBench** is a benchmarking tool for cloud/edge computing platforms that run microservice applications.
The tool creates *dummy* microservice applications that can be customized by the user and run on [Kubernetes](https://kubernetes.io) (and more).

µBench targets researchers and cloud platform developers who lack real microservice applications to benchmark their findings (e.g., new resource control mechanisms, AI-driven orchestration, etc.); µBench can create these applications for them. At the same time, µBench can also be used for educational purposes to show advantages and problems of microservice applications to students.

µBench allows users control some properties of the microservice application it creates, such as: the topology of the service mesh, the behaviors of composing microservices using a portfolio of stress functions (e.g. for CPU, memory, I/O, network) or implementing new ones, the microservice-to-microservice API (HTTP or gRPC), etc. 

After the microservice application is created, µBench is able to run it on a Kubernetes cluster; however, the µBench architecture is open to include other container execution platforms as well. Developers of these platforms can test their innovations by observing related effects on µBench-created applications, which export per-microservice metrics, such as delay, load, throughput, etc.

You can learn more about µBench [here](Docs/Manual.md)

This software is supported by:
- Liquid_Edge project, funded by Italian Ministry of University and Research within the PRIN 2017 program  
