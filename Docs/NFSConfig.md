# Configure NFS Server
µBench uses the NFS Server to share the configuration files among services, in particular 
the nfs shared directory (`/kubedata`) contains the `workmodel.json`, and a directory with the custom
internal functions.

## Install NFS Server
Install the **nfs-kernel-server** package on a node of the cluster, e.g. the K8s master node.

```bash
sudo apt update
sudo apt install nfs-kernel-server
```

Create the `/kubedata` directory that is shared among NFS clients and grant all permission to the contents inside the directory and the directory itself. 

```bash
sudo mkdir -p /kubedata
sudo chown nobody:nogroup /kubedata
sudo chmod 777 /kubedata
```

Edit the */etc/exports* file to grant the permissions for accessing the NFS server

```shell
/kubedata *(rw,sync,no_subtree_check,no_root_squash,insecure)
```

Finally export the NFS share directory and restart the NFS kernel server for the changes to come into effect

```bash
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
```

## Configure NFS Clients

Client nodes must have nfs-common package and a `/kubedata/mubSharedData` directory used to mount the NFS folder   

```bash
sudo mkdir /kubedata
sudo apt update
sudo apt install nfs-common
```

Edit the */etc/fstab* file to automount the NFS server folder automatically. Here we assumed that the IP address of the NFS server is 192.168.0.46

```bash
192.168.0.46:/kubedata /kubedata nfs defaults 0 2
```

Mount the shared directory to the client:
```bash
sudo mount 192.168.0.46:/kubedata /kubedata
```
To test the configuratin put a file in the folder of the NFS server node and see if client nodes can access it.
