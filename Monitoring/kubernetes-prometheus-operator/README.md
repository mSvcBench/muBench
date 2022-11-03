# Prometheus operator

You can install [Prometheus operator](https://github.com/prometheus-operator/prometheus-operator) via Helm ([install Helm](https://helm.sh/docs/intro/install)): 

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
[Istio](https://istio.io/) service mesh can be included in the cluster for a deeper monitoring.

(If you want to also install Jaeger jump to the optional section below)

To install Istio we used:

```zsh
export ISTIO_VERSION=1.15.2
curl -L https://istio.io/downloadIstio | sh -
cd istio-$ISTIO_VERSION
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

### Optional Jaeger Installation
Before to install Istio, we used the Istio provided basic [sample installation](https://istio.io/latest/docs/ops/integrations/jaeger/) to quickly get Jaeger up and running in the same namespace of istio (`istio-system`)

```zsh
wget https://raw.githubusercontent.com/istio/istio/release-1.15/samples/addons/jaeger.yaml
```
Edit the file just downloaded and replace the `ClusterIP` with a `NodePort` in the ***tracing*** Service 

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: tracing
  namespace: istio-system
  labels:
    app: jaeger
spec:
  type: NodePort
  ports:
    - name: http-query
      port: 80
      protocol: TCP
      targetPort: 16686
    - name: grpc-query
      port: 16685
      protocol: TCP
      targetPort: 16685
  selector:
    app: jaeger
```

If the namespace *istio-system* does not exist, create it and apply the edited yaml:

```zsh
kubectl create namespace istio-system
kubectl apply -f jaeger.yaml
```
Get the address of the *jaeger-collector* service and continue with the **Istio** installation:

```zsh
kubectl get service jaeger-collector -n istio-system
```

```zsh
export ISTIO_VERSION=1.15.2
curl -L https://istio.io/downloadIstio | sh -
cd istio-$ISTIO_VERSION
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo --set values.global.tracer.zipkin.address=<jaeger-collector-address>:9411 -y
kubectl label namespace default istio-injection=enabled
```

To get the NodePort on which the Jaeger UI is available use:
```zsh
kubectl get service tracing -n istio-system
```
![Jaeger UI](JaegerUI.png)

## Prometheus Monitor
Then it is necessary to add Prometheus PodMonitor and ServiceMonitor:
```zsh
kubectl apply -f istio-prometheus-operator.yaml
```

Istio may use [Metrics merging](https://istio.io/latest/docs/ops/integrations/prometheus/), therefore the µBench metrics can be shown two times, even though with different 'job' labels. To avoid this, in presence of Istio, can be convenient not to run the aforementioned µBench PodMonitor. 
