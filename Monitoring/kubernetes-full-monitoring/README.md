# Prometheus operator

You can install [Prometheus operator](https://github.com/prometheus-operator/prometheus-operator) via Helm ([install Helm](https://helm.sh/docs/intro/install)): 

```zsh
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

If Istio/Jaeger tools are not necessary, to get metrics from µBench services it is necessary to deploy the Prometheus `µBench PodMonitor` with
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
[Istio](https://istio.io/) service mesh can be included in the cluster for deeper monitoring.

To install Istio we used [Helm](https://istio.io/latest/docs/setup/install/helm/):

```zsh
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
kubectl create namespace istio-system
helm install istio-base istio/base -n istio-system
helm install istiod istio/istiod -n istio-system --wait
kubectl label namespace default istio-injection=enabled

kubectl create namespace istio-ingress
kubectl label namespace istio-ingress istio-injection=enabled
helm install istio-ingress istio/gateway -n istio-ingress --wait
```

## Integration with Prometheus
To expose Istio [metrics](https://istio.io/latest/docs/reference/config/metrics/) to Prometheus it is necessary to add Prometheus PodMonitor and ServiceMonitor:
```zsh
kubectl apply -f istio-prometheus-operator.yaml
```

Istio may use [Metrics merging](https://istio.io/latest/docs/ops/integrations/prometheus/), therefore the µBench metrics can be shown two times, even though with different 'job' labels. To avoid this, in presence of Istio, we have avoided to run install the µBench PodMonitor. 

## Jaeger Tracing
[Jaeger](https://www.jaegertracing.io/) can be used to monitoring a µBench application at trace-level. 
Istio is [integrated](https://istio.io/latest/docs/tasks/observability/distributed-tracing/jaeger/) with Jaeger, therefore to get Jaeger up and running it is enough to install Istio and then use the following Istio addon.

```zsh
kubectl apply -f jaeger.yaml
```
To expose Jaeger service as NodePort Service on port 30002 (HTTP) use

```zsh
kubectl apply -f jaeger-nodeport.yaml
```

## Kiali Istio Dashboard
[kiali](https://kiali.io/) can be used as Istio dashboard. To deploy kiali it is enough to deploy the next kiali resources, which include a kiali-nodeport NodePort service on port `30003` use.
```zsh
kubectl apply -f kilai.yaml
kubectl apply -f kilai-nodeport.yaml
```

