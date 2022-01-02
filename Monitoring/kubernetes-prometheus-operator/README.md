# kubernetes prometheus operator

You can install [Prometheus operator] (https://github.com/prometheus-operator/prometheus-operator) via helm: 

```zsh
kubectl create namespace monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

Deploy the PodMonitor with
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

