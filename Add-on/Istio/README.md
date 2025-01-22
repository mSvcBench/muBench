## Istio Destination Rule

`create-destination-rule` is a tool for generating Istio `DestinationRule` configuration files. `DestinationRule` objects are used to configure load balancing policies, outlier detection, and other traffic routing behaviors for services within an Istio service mesh. 

By using a `DestinationRule`, you can enable Istio's locality-based load balancing, which routes traffic to the nearest instance of a service based on the region, zone, and sub-zone of the node where the service is running. This feature is particularly useful in edge computing scenarios, where services are deployed across multiple regions, zones, and sub-zones.

This tool automates the creation of `DestinationRule` YAML files. It accepts the following parameters:
- `--in`: The input directory containing YAML files with the service definitions.
- `--out`: The output directory where the generated `DestinationRule` YAML files will be stored. If not specified, it defaults to the input directory.
- `--template`: A template file specifying the `DestinationRule` values, except for the fields `spec/host`, `metadata/name`, and `metadata/namespace`. These fields are automatically set to match the name and namespace of the corresponding service.

### Example Usage:
```zsh
python3 Add-on/Istio/create-destination-rule.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/dest-rule-yamls' --template 'Add-on/Istio/destination-rule-template.yaml' 
```

Once the `DestinationRule` files are generated, you can apply them to the cluster with the following command:
```zsh
kubectl apply -f SimulationWorkspace/dest-rule-yamls
```

---

## Istio Gateway and Virtual Service

To expose the `s0` microservice via the Istio ingress gateway, you need to apply the `istio-gateway.yaml` and `istio-s0-virtual-service.yaml` configuration files to your cluster. 

Before applying the `istio-gateway.yaml` file, ensure that the `istio` selector label in the file matches the `istio` label used by the specific version of the Istio ingress gateway in your cluster. You can verify this by inspecting the YAML file of the ingress gateway pod.

```zsh
kubectl apply -f Add-on/Istio/istio-gateway.yaml -n <application-namespace>
kubectl apply -f Add-on/Istio/istio-s0-virtual-service.yaml -n <application-namespace>
```

Replace `<application-namespace>` with the namespace of your application.

This setup configures the Istio ingress gateway to route external traffic to the `s0` microservice.

## Grafana Dashboard
The `grafana-dashboard.json` file contains a sample Grafana dashboard configuration for monitoring the applications. You can import this dashboard into your Grafana instance to visualize the metrics collected by Prometheus.
Be careful of configuring the `ns` variable in the dashboard to match the namespace of your application and of istio-ingress e.g.,
```json
default|istio-ingress
```
Besides, you can configure the istio ingress label exported by Prometheus with the variable `istio_ingress_prometheus_label`, e.g.,
```json
istio-ingressgateway
```