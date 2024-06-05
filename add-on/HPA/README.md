## create-hpa

`create-hpa` is a tool that generates Kubernetes HorizontalPodAutoscaler configuration files. The tool takes as parameters an input directory where there are YAML files with the Deployment definitions, an output directory where new YAML files with the HorizontalPodAutoscaler definitions will be placed, and an HPA template file that specifies HPA parameters except the name `metadata/name` and `scaleTargetRef/name` values that will be set as equal to the name of the Deployment.

Examples:
```zsh
python3 add-on/Istio/create-destination-rule.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/dest-rule-yamls' --template 'add-on/edge-computing/destination-rule-template.yaml' 
```

