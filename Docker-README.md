# µBench Docker Image

This image contains:

- µBench software of this folder
- kubectl
- helm
- Apache ab tools for benchmarking
- vim, nano, iproute2, iputils-ping

To build you could use:

```zsh
docker build -t msvcbench/mubench .
```

Copy `.kube/config` into `/root/.kube/config` container folder to access Kubernetes cluster from the container. In case update the `server:` key with the correct IP address. 
Be careful to use the correct K8s dns service url in `Configs/K8sParameters.json`

To run the container you could use 

```zsh
docker run -it --rm --name mubench -v /path/to/your/.kube/config:/root/.kube/config msvcbench/mubench
```

Then access the container with:

```zsh 
docker exec -it mubench /bin/bash
```

Be careful to use the correct K8s DNS in use in your cluster (kube-dns, coredns) service url in `Configs/K8sParameters.json`

>__**Note**__: This Dockerfile doen't build the ServiceCell software. To build the ServiceCell software, use the Dockerfile in the ServiceCell folder.