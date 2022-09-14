# Microservice cell abstraction
The main code of a service-cell is the `CellController` which exposes the REST API (via gunicorn or Flask) and the gRPC API. In turn, it uses other functions to run the internal service (`InternalServiceExecutor`) and, then, the external services (`ExternalServiceExecutor`). The external services use parallel threads (single-process) in the case of parallel requests to downstream services in the mesh.  

Currently, this repository containse the v3 service-cell implementation.

## Multi-process service cell (v3)
The v3 service cell image can be built using the `Dockefile.debug-mp` . This version uses Gunicorn WSGI for REST services. Each REST request is served by a pool of processes and threads according to the `workers` and `threads` keys in `workmodel.json`. Therefore, at most this service-cell uses a number of CPU cores equal to `workers`. In the case of gPRG, this service-cell uses only one core (single worker). So multi-process experiments can only be performed using the REST request method.

The Docker image of this service-cell is  `msvcbench/microservice_v3-screen:latest` 