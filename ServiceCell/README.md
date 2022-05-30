# Microservice cell abstraction
The main code of a service-cell is the `CellController` which exposes the REST API (via gunicorn or Flask) and the gRPC API. In turn, it uses other functions to run the internal service (`InternalServiceExecutor`) and, then, the external services (`ExternalServiceExecutor`). The external services use parallel threads (single-process) in the case of parallel requests to downstream services in the mesh.  

Currently, we have two service-cell implementations.

## Single-process service cell (v2)
The v2 service-cell image can be built using the `Dockefile` or the `Dockefile.debug`. This version uses Flask WSGI for REST services. Each request is served on a different thread, but all requests are served by the same process (single worker). Therefore, at most this service-cell uses a single CPU core. The same is happening with gPRC. 

When this image is used the `workers` key of the `workmodel.json` is not used and the number of `threads` is respected only for gRPC request method. In the case of REST, the threads used are the maximum allowed by the operating system (Flask does not allow to control of this parameter).

The debug version runs the python code in a Linux screen for easy debugging. If the program crashes, the container will not crash, so errors can be inspected, but (beware) Kubernetes will not be aware of this, so it will not re-deploy crashed pods. 

The Docker images of this service-cell are  `msvcbench/microservice_v2:latest` and `msvcbench/microservice_v2-screen:latest` 

## Multi-process service cell (v3)
The v3 service cell image can be built using the `Dockefile.debug-mp` . This version uses Gunicorn WSGI for REST services. Each REST request is served by a pool of processes and threads according to the `workers` and `threads` keys in `workmodel.json`. Therefore, at most this service-cell uses a number of CPU cores equal to `workers`. In the case of gPRG, this service-cell uses only one core (single worker). So multi-process experiments can only be performed using the REST request method.

The Docker image of this service-cell is  `msvcbench/microservice_v3-screen:latest` 