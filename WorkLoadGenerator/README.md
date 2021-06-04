# Workload Generator

The WorkLoadGenerator creates the scheduling of the simulation.

It defines the time steps of the simulated requests, as well as which service to reach at each time step.

It requires as input the `WorkLoadParameters.json` and generates the `workload.json` file that is needed for the [Runner](/Runner/README.md) to perform a simulation.

## Input Parameters

The `ingress_service` parameter indicates the name of the service that acts as the ingress service, in this example `s0`.
As `request_parameters`, you need to specify, in *ms*, the mean of the negative exponential you want to simulate between each request with `mean_interarrival_time`. Also, you must specify the last step of the duration of the simulation with `stop_event`.
The `WorkLoadGenerator` will generate a file called `workload.json` and it will save it to the path specified from the `OutputPath` parameter.

```json
{
   "WorkLoadParameters":{
      "ingress_service":"s0",
      "request_parameters": {
         "mean_interarrival_time": 500,
         "stop_event": 1000
      }
   },
   "OutputPath": "../SimulationWorkspace"
}
```

## Output Understanding

Each line of the `workload.json` file binds a time step in *ms* to the service to send the request.

```json
[
  {"time": 0,"service": "s0"},
  {"time": 68,"service": "s0"},
  {"time": 72,"service": "s0"},
  {"time": 1062,"service": "s0"},
  {"time": 2147,"service": "s0"},
  {"time": 2230,"service": "s0"}
]
```

## Run the script
Edit the `WorkLoadParameters.json` file before running the `WorkLoadGenerator`.

Finally, run the script to obtain and save to the `OutputPath` the `workload.json` as follows:
```
python3 RunWorkModelGen.py
```