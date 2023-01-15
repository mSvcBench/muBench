# µBench Docker Image

This image contains 

- µBench software of this folder
- kubectl
- helm
- Apache ab tools for benchmarking
- vim, nano, iproute2, iputils-ping

To build you could use 

```zsh
docker build -t msvcbench/mubench .
```

Copy `.kube/config` into `/root/.kube/config` container folder to access Kubernetes cluster from the container.
