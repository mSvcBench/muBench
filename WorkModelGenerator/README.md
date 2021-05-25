# Work Model Generator

The WorkModelGenerator creates the `workmodel.json` json file where it associates for each service of the microservice application its internal job function.

Edit the `RunWorkModelGen.py` python file before running it.
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