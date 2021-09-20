# How to write custom function
## What is a custom function

Each service of the microservice mesh executes an internal-service when called and by default it uses the `compute_pi` function. 
The default function keeps the CPU busy depending on the specified complexity of operations.

To try other scenarios, you can use your own specific functions to stress the aspect you whish to simulate: CPU, memory or storage. 
In order to do so, you must write your own python function and save it to the subfolder `InternalServiceFunctions` inside your NFS shared directory.
If you followed our [NFS configuration](NFSConfig.md), create the subfolder into `/mnt/mubSharedData` using 
`mkdir /mnt/mubSharedData/InternalServiceFunctions`, otherwise create it according to your NFS configurations.

## How to write your own custom job

- As input, your function receives a dictionary with the parameters specified in the [work model generator](../WorkModelGenerator/README.md).
- As output, your function must return a string used as body for the response given back by a service.

> Note: each custom function must have a unique name, otherwise conflicts will occur.
Also, you can specify more than one custom function inside the same python file.

```python
def custom_function(params):
    
    ## your code here

    ## the response of the function must be a string
    response_body = "the body must be a string"

    return response_body
```
