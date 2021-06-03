# K8s Autopilot
The K8s autopilot is an easy way to deploy all the component of the MicroServiceSimulator. It's work under two assumptions:
* Run the K8s autopilot script on the K8s Master Node
* The [NFS server](/Docs/NFSConfig.md) must have been configured on the same K8s Master Node

## Run K8s Autopilot
Before running the script edit the configuration file `K8sAutopilotConf.py`. This file contains the configurations of all other modules seen in the [example](/Docs/Example.md).  

* The only parameter that you must edit in this file is `nfs_conf` parameters with both the IP address and shared folder path of the NFS server.

```python
nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}
```
* Then, you can run the `K8sAutopilot.py` script:

```shell
python3 K8sAutopilot.py
```

* add workflow drawio:
 
TODO

    * Properly edit the K8sAutopilotConf file
    * Run K8s autopilot, it check if there is a deployment yet. 
      * Yes -> asks for undeploy, if yes delete the deployment and remove yaml files
      * No -> Generate yaml files and deploy
        
    * Asks to generate the workload file
    * DONE! :)
