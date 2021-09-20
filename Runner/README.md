# Runner

The `Runner.py` is in charge of executing one or more *workloads* and save the test results as an output file.

It is advisable to execute the `Runner` outside the nodes of the cluster where the microservices application is deployed, with the purpose of not holding resources from the running services and bias the test results.
> Be careful of the network delays between the executor of the `Runner` and the microservice application's gateway.

The `Runner` schedules the events defined by the `workload` files and then a thread pool executes HTTP requests to the associated `service` through the access gateway.
We recall the structure of a `workload` file:

```json
[
  {"time": 100, "service": "s0"},
  {"time": 200, "service": "s0"},
  {"time": 500, "service": "s0"},
  {"time": 700, "service": "s0"},
  {"time": 900, "service": "s0"},
  {"time": 1000, "service": "s0"}
]
```

For instance, in this case the Runner sends an HTTP request to s0 at time 100,200,... etc.

## Input Parameters 

Edit the `RunnerParameters.json` file before executing `Runner.py`. We use the next example to explain the related parameters.

```json
{
   "RunnerParameters":{
      "ms_access_gateway": "http://<access-gateway-ip>:<port>",
      "workload_files_path_list": ["/path/to/workload.json"],
      "workload_rounds": 1,
      "thread_pool_size": 4,
      "result_file": "result.txt"
   },
   "OutputPath": "../SimulationWorkspace",
   "AfterWorkloadFunction": {
   "file_path": "Function",
   "function_name": "get_prometheus_stats"
   }
}
```

The HTTP requests are sent towards the services through the access gateway, whose IP address is specified in the `ms_access_gateway` parameter.
The workload files can be specified into the `workload_files_path_list` parameter as the path of a single file generated with the [WorkLoadGenerator](/WorkLoadGenerator/README.md) or as the path of a directory where multiple files are saved.
In this way, you can simulate different scenarios one after the other.

Specifically, the `Runner` will sequentially execute one by one all of the files inside this directory and save the test results file with the name `result_file`, to the output directory `OutputPath`.
Also, you can specify how many times you want to cycle through the workload directory with the `workload_rounds` parameter, as well as the size of the thread pool allocated for each test with `thread_pool_size`.

After each test, the `Runner` can execute the custom python function (e.g. to fetch monitoring data from Prometheus) specified in the key `file_name`, which is defined by the user in a file specified into the `file_path` key. 


## Output Understanding

As a result, we obtain a file called as the `result_file`, in this case `result.txt`, with three columns: the first one indicates the time of the execution of the request as a unix time stamp; the second column indicates the elapsed time, in *ms*, of the request; the third column reports the received HTTP status (e.g. 200 OK).


```bash
1622712602765 	 0.163079   200
1622712603940 	 0.158704   200      
1622712604272 	 0.147043   200
1622712605857 	 0.14741    200
1622712606245 	 0.155425   200
1622712606612 	 0.161511   200
1622712606972 	 0.15307    200
1622712607343 	 0.157438   200
1622712607520 	 0.147363   200
1622712607593 	 0.192539   200
...
```


## Install requirements
To execute the `Runner`, first install the global requirements in the main folder using ``pip3``:

```zsh
pip3 install -r requirements.txt
```

---
## Run the script
Edit the `RunnerParameters.json` file before executing the `Runner`.

Finally, run the script to obtain the `result_file` saved to the `OutputPath`.
You can specify your custom configuration file as argument otherwise, if you do not indicate any argument, it will use the default configuration file (`RunnerParameters.json`) located inside its directory:

```zsh
python3 Runner.py [PARAMETER_FILE]
```
