# Configure NFS Server
The MicroServiceSimulator use the NFS Server to share the configuration files between services, in particular 
the nfs shared directory contains the work model and service mesh files, and a directory with the optional
internal job functions.

## Install NFS Server
For simplicity and compatibility with the K8s Autopilot script. 
1. We will install the **nfs-kernel-server** package on the master node.

```bash
sudo apt update
sudo apt install nfs-kernel-server
```

2. We will be creating a directory that will be shared among client systems and we grant all permission to the 
   content inside the directory and the directory itself. 
   This is also referred to as the export directory and it’s in this directory that we shall 
   later create files which will be accessible by client systems.
```bash
sudo mkdir -p /kubedata/mubSharedData
sudo chown nobody:nogroup /kubedata/mubSharedData
sudo chmod 777 /kubedata/mubSharedData
```

3. Edit the */etc/exports* file to grant the permissions for accessing the NFS server
```shell
/kubedata/mubSharedData pod_subnet(rw,sync,no_subtree_check,no_root_squash,insecure)
/kubedata/mubSharedData node_subnet(rw,sync,no_subtree_check,no_root_squash,insecure)
```
Edit this two params according to your configuration:
* **node_subnet:** Subnet of K8s nodes (e.g. 10.3.0.0/24)
* **pod_subnet:** Subnet of K8s pods (e.g. 10.244.0.0/16)

4. Finally export the NFS share directory and restart the NFS kernel server for 
   the changes to come into effect

```bash
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```