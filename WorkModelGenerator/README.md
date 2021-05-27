# Work Model Generator

## Work Model
The working model defines which internal services are executed by the Microservice Application services. To allow the continuous integration of new internal services, the internal services are python functions to be placed in the NFS_SHARED_FOLDER. In addition, any service-cell incorporates a default `compute_pi` function that computes a configurable number of python decimal digits. A service uses one of these possible functions as an internal-service, and the choice is made during generation of the working model file according to configurable probabilites that can be given to any python function.

## Internal-service model
A function that implements an internal-service can do some work such as, dummy calculations, read/write operations, etc. At the end of these jobs, the function returns a dummy amount of kBytes in a string, which will be sent back to the service caller after both the internal-service and external-services are completed.
Thus, by appropriately designing an internal-service function, we are able to decide what to stress, including the CPU, I/O, or network. 
Each function takes some user-defined parameters as input and must return a string.  

## compute_pi
The built-in function `compute_pi` computes an `N` number of decimals of the π, where `N` is a integer, randomly chosen in an interval [`X`,`Y`] for each execution. The larger the interval, the greater the complexity and the stress on the CPU. After the computation, the `compute_pi` function returns a dummy string made of `B` kBytes, where `B` is a sample of an exponential random variable whose average is the `mean_bandwidth` parameter.    
So the input parameters of `compute_pi` are:
- `"range_complexity": [X, Y]`  
- `"average_bandwidth": value`
    
## Output Undersanding
The `WorkModelGenerator.py` creates the `workmodel.json` file that describes the work model, i.e. which is the internal-service of any service with related parameters.
```json
{ "s0": {"internal-service": 
 { "compute_pi": { 
    "mean_bandwidth": 11,
    "range_complexity": [101, 101]
    }
 }
}
```     
This is an example of a part of a produced `workmodel.json` that related to the service s0. The internal-service of s0 is the function `compute_pi` that takes as input two parameters, namely `mean_bandwidth` and `range_complexity`. Other custom functions stored in the NFS_SHARED_FOLDER can use user-defined parameters (see e.g. colosseum.py that has to be copied in NFS_SHARED_FOLDER). 

## Input parameters
Edit the `WorkModelParameters.json` python file before running it .
As input, you must specify the path of the service mesh json file. Follow [these instructions](../ServiceMeshGenerator/README.md) if you haven't already created the file.

```python
servicemesh_file_path = "path/to/servicemesh.json"
```

Also, you must specify a dictionary with all the functions for the internal jobs, its related probability of been chosen, along with all the specific function parameters.

For example, the `compute_pi` function is available by default and its job is to keep the CPU busy computing the _pi_ constant. 
The complexity of the computation depends on the number of _pi_ decimals asked to compute and it is indicated by the `range_complexity` parameter. 
The size of the function response is given by a negative exponential distribution with mean equal to `mean_bandwidth`.


> Note: all the custom functions must exist and must be available inside the [NFS shared directory](../Docs/CustomJobs.md).


For example:
```json
parameters = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [101, 101]},
              "custom_function": {"probability": 0.6, "function_param1": 13, "function_param2": 42}
              }

servicemesh_file_path = "../ServiceMeshGenerator/servicemesh.json"
```

---
## Run the script
Finally, to run only the WorkModelGenerator, run the following script:

```
python3 RunWorkModelGen.py
```