# Prometheus manual installation 

Run the following commands:

```bash
kubectl create namespace monitoring
kubectl apply -f Monitoring/kubernetes-prometheus
```
Prometheus server will be available at: `http://<access-gateway-ip>:30000` after the successful deployment of the following commands: