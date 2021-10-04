# Micro Service Cell Abstraction

## Docker Build

If you need to edit the Cell image, you can do it by executing the following commands:

```bash
docker build -t <docker-hub-user>/<repo-name>:<tag> .
```

Also, if you want to push your images to the [Docker Hub](https://hub.docker.com/) registry you can do it by running:

```bash
docker push <docker-hub-user>/<repo-name>:<tag>
```

> Note: if you change the name of the docker image Cell, remember to edit the `image` entry on the `K8sParameters.json` of the [K8sYamlBuilder](/Docs/Kubernetes/K8sYamlBuilder) parameter file.