## create-destination-rule

`create-destination-rule` generates Istio DestinationRule configuration files. DestinationRules are used to configure load balancing policies, outlier detection, and other traffic routing behaviors for services in an Istio service mesh. With a DestinationRule it is possible to enable IStio locality load balancing that allows to route traffic to the closest instance of a service based on the region, zone, and sub-zone of the node where the service is running. Accordingly, it is useful for edge computing scenarios where services are deployed in different regions, zones, and sub-zones.
This tool helps to automate the process of creating these DestinationRules YAML files.
It takes as parameters an input directory of YAML files (`--in`) with the Service definitions, an output directory (`--out`) where to insert DestinationRules YAMLS for each Service and a template file (`--template`) describing the DestinationRules values to be used except the value `spec/host` and `metadata/name` that will be set as equal to the name of the Service. If the output directory is not specified it is equal to the input one.

Examples:
```zsh
python3 Add-on/Istio/create-destination-rule.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/dest-rule-yamls' --template 'Add-on/Istio/destination-rule-template.yaml' 
```

