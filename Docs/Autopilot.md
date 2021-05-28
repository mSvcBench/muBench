# Autopilot
The autopilot is an easy way to deploy all the component of the MicroServiceSimulator. It's work under two assumptions:
* Run the autopilot script on the K8s Master Node
* The [NFS server](/Docs/NFSConfig.md) must have been configured on the same K8s Master Node

## Run AutoPilot
Before running the script edit the configuration file `AutoPilotConf.py`. This file contains the configurations of all other modules seen in the [example](/Docs/Example.md).  

* The only parameter that you must edit in this file is `nfs_conf` parameters with both the IP address and shared folder path of the NFS server.

```python
nfs_conf = {"address": "10.3.0.4", "mount_path": "/mnt/MSSharedData"}
```
* Then, you can run the `AutoPilot.py` script:
```shell
python AutoPilot.py
```

* add workflow drawio:
 
TODO

    * Properly edit the AutoPilotConf file
    * Run autopilot, it check if there is a deployment yet. 
      * Yes -> asks for undeploy, if yes delete the deployment and remove yaml files
      * No -> Generate yaml files and deploy
        
    * Asks to generate the workload file
    * DONE! :)
