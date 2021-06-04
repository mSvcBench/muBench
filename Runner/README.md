# Runner

The `Runner.py` is in charge of executing one or more *workloads* and save the simulation results as an output file.

It is advisable to execute the `Runner` outside the nodes of the cluster where the microservices application is deployed, with the purpose of not holding resources from the running services and bias the simulation results.
> Be careful of the network delays between the executor of the `Runner` simulator and the microservice application's gateway.

The `Runner` schedules the events defined by the `workload` files and then a thread pool executes the requests to the associated `service` through the access gateway.
We recall the structure of a `workload`:

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

## Input Parameters 

Edit the `RunnerParameters.json` file before executing `Runner.py`. We use the next example to explain the related parameters.

```json
{
   "RunnerParameters":{
      "ms_access_gateway": "http://<access-gateway-ip>",
      "workload_files_path_list": ["/path/to/workload.json"],
      "workload_rounds": 1,
      "thread_pool_size": 4,
      "result_file": "result.txt"
   },
   "OutputPath": "../SimulationWorkspace"
}
```

The requests are sent towards the service of the application, in this case `s0`, that is accessible through the access gateway, which IP address is specified from the `ms_access_gateway` parameter.
The workload files can be specified into the `workload_files_path_list` parameter as the path of a single file generated with the [WorkLoadGenerator](/WorkLoadGenerator/README.md) or as the path of a directory where multiple files are saved.
In this way, you can simulate different scenarios one after the other.

Specifically, the `Runner` will sequentially execute one by one all of the files inside this directory and save the simulation result file with the name `result_file`, to the output directory `OutputPath`.
Also, you can specify how many times you want to cycle through the workload directory with the `workload_rounds` parameter, as well as the size of the thread pool allocated for each simulations with `thread_pool_size`.


## Output Understanding

As a result, we obtain a file called as the `result_file`, in this case `result.txt`, with two columns: the first one indicates the time of the execution of the request as a unix time stamp while the second column indicates the elapsed time, in *ms*, of the request.


```bash
1622712602765 	 0.163079
1622712603940 	 0.158704
1622712604272 	 0.147043
1622712605857 	 0.14741
1622712606245 	 0.155425
1622712606612 	 0.161511
1622712606972 	 0.15307
1622712607343 	 0.157438
1622712607520 	 0.147363
1622712607593 	 0.192539
...
```


## Install requirements
To execute the `Runner`, first install the requirements using ``pip3``:

```zsh
pip3 install -r requirements.txt
```

---
## Run the script
Edit the `RunnerParameters.json` file before executing the `Runner`.

Finally, run the script to obtain the `result_file` saved to the `OutputPath` as follows:

```zsh
python3 Runner.py
```
