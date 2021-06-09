# Work Model Generator

The working model defines which internal-services are executed by the Microservice Application services. To allow the continuous integration of new internal services, the internal services are python functions to be placed in python files of the `NFS_SHARED_FOLDER/InternalServiceFunction`. In addition, any service-cell incorporates a default `compute_pi` function that computes a configurable number of python decimal digits. A service uses one of these possible functions as an internal-service, and the choice is made during generation of the working model file according to configurable probabilities that can be given to any python function.

### Internal-service model
A function that implements an internal-service can do some work such as, dummy calculations, read/write operations, etc. At the end of these jobs, the function returns a dummy amount of kBytes in a string, which will be sent back to the service caller after both the internal-service and external-services are completed.
Thus, by appropriately designing an internal-service function, we are able to decide what to stress, including the CPU, I/O, or network. 
Each function takes some user-defined parameters as input and must return a string.  

### compute_pi
The built-in function `compute_pi` computes an `N` number of decimals of the π, where `N` is a integer, randomly chosen in an interval [`X`,`Y`] for each execution. The larger the interval, the greater the complexity and the stress on the CPU. After the computation, the `compute_pi` function returns a dummy string made of `B` kBytes, where `B` is a sample of an exponential random variable whose average is the `mean_bandwidth` parameter.    
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
      }
  },
  "s1": {
      "internal_service": {
         "colosseum": {}
      }
   }
}
```

This is an example of a part of a produced `workmodel.json` related to a service mesh composed of two services: `s0` and `s1`. The internal-service of `s0` is the function `compute_pi` that takes as input two parameters, namely `mean_bandwidth` and `range_complexity`. 
Instead, for the service `s1`, the custom function `colosseum` is associated to it.
Other custom functions are stored in python files located into the subfolder of the [NFS shared directory](/Docs/NFSConfig.md) `NFS_SHARED_FOLDER/InternalServiceFunction` with the possibility of using user-defined parameters (see e.g. `colosseum.py` [here](/Docs/MicroserviceModel.md#Custom-Functions)). 

### Input Parameters
Edit the `WorkModelParameters.json` file before executing `RunWorkModelGen.py`. The next example is given to explain its related parameters.

As input, you must specify for the `ServiceMeshFilePath` key, the path of the `service-mesh` json file. Follow [these instructions](/ServiceMeshGenerator/README.md) if you haven't already created such file.

Also, you must specify the `WorkModelParameters` whose values are the set of internal-service functions along with their parameters, which must include the `probability` key, used by the WorkModelGenerator for choosing which internal-service function assign to each service.
In the following example, the Work Model assigns to a service the default `compute_pi` as internal-service with a 40% probability, whilst the custom function `colosseum` is chosen with a 60% probability.

As input, it takes the `servicemesh.json` file located at the path specified by the `ServiceMeshFilePath` parameter, and saves the `workmodel.json` output file to the `OutputPath`.

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
      }
   },
   "ServiceMeshFilePath": "../SimulationWorkspace/servicemesh.json",
   "OutputPath": "../SimulationWorkspace"
}
```

---
## Run the script
Edit the `WorkModelParameters.json` file before running the `WorkModelGenerator`. 
Then, run the script to obtain `workmodel.json` as follows:

```
python3 RunWorkModelGen.py
```