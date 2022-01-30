# Prometheus operator

You can install [Prometheus operator] (https://github.com/prometheus-operator/prometheus-operator) via helm: 

```zsh
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

Deploy the Prometheus µBench PodMonitor with
```zsh
kubectl apply -f ./mub-monitor.yaml
```

To expose Prometheus server as NodePort service on port `30000` use

```zsh
kubectl apply -f ./prometheus-nodeport.yaml -n monitoring
```

To expose Grafana server as NodePort service on port `30001` use

```zsh
kubectl apply -f ./grafana-nodeport.yaml -n monitoring
```

Grafana `admin` password can be obtained with

```zsh
kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" -n monitoring | base64 --decode ; echo
``` 

# Istio
[Istio] (https://istio.io/) service mesh can be included in the cluster for a deeper monitoring.

To install Istio we used:

```zsh
 curl -L https://istio.io/downloadIstio | sh -
 curl -L https://istio.io/downloadIstio | sh -
 cd istio-1.12.2/
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
``` 

Then it is necessary to add Prometheus PodMonitor and ServiceMonitor:
```zsh
k apply -f istio-prometheus-operator.yaml
```

Istio may use [Metrics merging] (https://istio.io/latest/docs/ops/integrations/prometheus/), therefore the µBench metrics can be shown two times, even though with different 'job' labels. To avoid this, in presence of Istio, can be convenient not to run the aforementioned µBench PodMonitor. 
