# Work Model Generator

The working model defines which internal-services are executed by the Microservice Application services. To allow the continuous integration, the internal services are python functions stored into the NFS shared directory `NFS_SHARED_FOLDER/InternalServiceFunction`. In addition, any service-cell incorporates a default `compute_pi` function that computes a configurable number of python decimal digits. A service uses one of these possible functions as an internal-service, and the choice is made during generation of the work model file according to configurable probabilities given to any python function.

### Internal-service model
A function that implements an internal-service can do some work such as, dummy calculations, read/write operations, etc. At the end of these jobs, the function returns a dummy amount of kBytes in a string, which will be sent back to the service caller after both the internal-service and external-services are completed.
Thus, by appropriately designing an internal-service function, we are able to decide what to stress, including the CPU, I/O, or network. 
Each function takes some user-defined parameters as input and must return a string.  

### compute_pi
The built-in function `compute_pi` computes an `N` number of decimals of the *π*, where `N` is a integer, randomly chosen in an interval [`X`,`Y`] for each execution. The larger the interval, the greater the complexity and the stress on the CPU. After the computation, the `compute_pi` function returns a dummy string made of `B` kBytes, where `B` is a sample of an exponential random variable whose average is the `mean_bandwidth` parameter.    
So the input parameters of `compute_pi` are:
- `"range_complexity": [X, Y]`  
- `"average_bandwidth": value`
    
### Output Understanding
The `WorkModelGenerator.py` creates the `workmodel.json` file that describes the work model, i.e. which is the internal-service of any service with related parameters.

```json
{
  "s0": {
      "internal_service": {
         "compute_pi": { 
            "mean_bandwidth": 11,
            "range_complexity": [101, 101]
         }
      },
      "request_method": "rest",
      "url": "s0.default.svc.cluster.local",
      "path": "/api/v1",
      "image": "msvcbench/microservice_v2:latest",
      "replicas": 2
      "namespace": "default"
  },
  "s1": {
      "internal_service": {
         "colosseum": {}
      },
      "request_method": "rest",
      "url": "s1.default.svc.cluster.local",
      "path": "/api/v1",
      "image": "msvcbench/microservice_v2:latest",
      "namespace": "default"
   }
}
```

This is an example of a part of a produced `workmodel.json` related to a service mesh composed of two services: `s0` and `s1`. The internal-service of `s0` is the function `compute_pi` that takes as input two parameters, namely `mean_bandwidth` and `range_complexity`. 
Instead, for the service `s1`, the custom function `colosseum` is associated to it.
Other custom functions are stored in python files located into the subfolder of the [NFS shared directory](/Docs/NFSConfig.md) `NFS_SHARED_FOLDER/InternalServiceFunction` with the possibility of using user-defined parameters (see e.g. `colosseum.py` [here](/Docs/MicroserviceModel.md#Custom-Functions)). 
Furthermore, each service is aware, through the `request_method` key, of which synchronous request/response-based communication mechanisms it uses, such as HTTP-based REST or gRPC, the `url` used together with the `path` to listen to requests of connected services.
Finally, the `image` parameter indicates the image of the service used when it is deployed, for example to the K8s cluster, and in this case even the `namespace` is used.


### Input Parameters
Edit the `WorkModelParameters.json` file before executing `RunWorkModelGen.py`. The next example is given to explain its related parameters. 

As input, you must specify for the `ServiceMeshFilePath` key, the path of the `service-mesh` json file. Follow [these instructions](/ServiceMeshGenerator/README.md) if you haven't already created such file.

Also, you must specify the `WorkModelParameters` whose values are the set of internal-service functions along with their parameters, which must include the `probability` key, used by the WorkModelGenerator for choosing which internal-service function assign to each service. Another optional key is `replicas` for choosing the number of replicas of the internal-service. Other keys are used by the specific internal-service function, e.g., the `compute_pi` function uses `mean_bandwidth` and `range_complexity`.

Furthermore, you can list database-specific functions if you leave the `"type": "database"` property inside the function name key you want to use for the database services, in this case `databases_function`.

In the following example, the Work Model assigns to a service the default `compute_pi` as internal-service with a 40% probability, whilst the custom function `colosseum` is chosen with a 60% probability, as well as the database-specific function named `databases_function`.

You need to specify also the protocol of communication used between the services: `rest` or `grpc`, as the example below.
Lastly, the `databases_prefix` is used to personalize the names of the services used as database, i.e. we used `sdb`, so the databased will be created with the names `sdb1`, `sdb2`, etc.

As input, the Work Model Generator takes the `servicemesh.json` file located at the path specified by the `ServiceMeshFilePath` parameter, and saves the `workmodel.json` output file to the `OutputPath`.

```json
{
   "WorkModelParameters":{
      "compute_pi":{
         "probability":0.4,
         "mean_bandwidth":11,
         "range_complexity":[101, 101]
      },
      "colosseum": {
         "probability": 0.6
      },
      "databases_function": {
         "type": "database",
         "probability": 0.6
      },
      "request_method": "gRPC",
      "databases_prefix": "sdb"
   },
   "ServiceMeshFilePath": "../SimulationWorkspace/servicemesh.json",
   "OutputPath": "../SimulationWorkspace"
}
```

---
## Run the script
Finally, run the script to obtain `workmodel.json`.
You can specify your custom configuration file as argument otherwise, if you do not indicate any argument, it will use the default configuration file (`WorkModelParameters.json`) located inside its directory:

```zsh
python3 RunWorkModelGen.py [PARAMETER_FILE]
```
