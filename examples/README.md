# Examples

This folder contains some `workmodel.json` files created using the [WorkModelGenerator](../WorkModelGenerator/) and used to generate applications to benchmark.

In particular, to study the impact of splitting the application workload into services, we generated applications with increasing number of microservices (N), from 1 (monolithic) to 10, and are configured as follows:
* the service-mesh has the star topology in Fig. 1b and the links’ probabilities are all equal to 1, therefore all the microservices are involved for each user request;
* users send requests to the microservice `s0`, which in turn calls all the other N − 1 downstream microservices, either in **sequence** or in **parallel**;
* the inter-service communications use the HTTP/REST model;
* the internal-service run by the N microservices is the same. It is the `loader` function, presented [here](/Docs/Manual.md#Work-Model-Generator). It is configured to transmit back 100 kB, stress only the CPU by computing 100 digits of Pi (π) and repeating this computation 100/N times. The overall amount of π digits computed by the application is 100,000 independently of N. Thus we can make a computation-fair comparison versus N microservices.

<p align="center">
<img width="200" src="servicemeshA.png"> 
<img width="200" src="servicemeshB.png">
<img width="200" src="servicemeshC.png">
<img width="200" src="servicemeshD.png">
<figcaption align = "center"><b>Fig. 1 - Different application topologies with 20 microservices, namely (from left to rigth) A, B, C and D.</b></figcaption>
</p>

We also generated other 4 applications with 20 microservices with the same workload but with different microservice mesh topologies, namely the ones in Fig. 1: A, B, C, D.

Additionally, the topology C has a `workmodelC-multi.json` with introduced randomness in spanning the mesh for serving a request and heterogeneity in internal-services. Specifically:
* we used a probability equal to 0.5 for each link of the mesh, with the exclusion of links `s0`-`s3`) and `s3`-`s8`, for which we used a probability equal to 1. Therefore, `s0`, `s3` and `s8` are involved in any user request.
* the microservice `s8` is the only one that stresses the CPU. 
* the microservice `s0` does not perform any internal-service
* the other microservices either load the memory or the disk with read/write operations.
