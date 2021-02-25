# MicroServiceSimulator

* Configurare NFS Server su masterNode

* Gen ServiceMesh
* Gen WorkModel
  
* Copiare ServiceMesh, WorkModel e JobFunctions nella cartella dell'NFS

    * Avviare K8sYamlBuild
    * kapp yaml/PersistentVolumeMicroService.yaml
    * kapp yaml/ConfigMapNginxGw.yaml
    * kapp yaml/DeploymentNginxGw.yaml
    * kapp K8sYamlBuild/yamls/

* Interrogare nxgin gateway -> http://IP_CLUSTER:31113/SERVICE_NAME (es. http://n1:31113/s0, 
  http://n1:31113/s1 ...)
