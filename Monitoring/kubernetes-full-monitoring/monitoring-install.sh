# Secure .kube
chmod go-r -R ~/.kube/

# Prometherus
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring

# Prometheus (30000) and Grafana (30001) NodePort Services
kubectl apply -f prometheus-nodeport.yaml -n monitoring
kubectl apply -f grafana-nodeport.yaml -n monitoring

# Istio
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
kubectl create namespace istio-system
helm install istio-base istio/base -n istio-system
helm install istiod istio/istiod -n istio-system --wait
kubectl create namespace istio-ingress
kubectl label namespace istio-ingress istio-injection=enabled
helm install istio-ingress istio/gateway -n istio-ingress

# Istio - Prometeus integration
kubectl apply -f istio-prometheus-operator.yaml

# Jarger
kubectl apply -f jaeger.yaml

# Jaeger NodePort Service (30002)
kubectl apply -f jaeger-nodeport.yaml

#Kiali
kubectl apply -f kiali.yaml

#Kiali NodePort Service (30003)
kubectl apply -f kiali-nodeport.yaml

