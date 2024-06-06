## create-hpa

`create-hpa` is a tool that generates Kubernetes HorizontalPodAutoscaler configuration files. The tool takes as parameters an input directory (`--in`) where there are YAML files with the Deployment definitions, an output directory (`--out`) where new YAML files with the HorizontalPodAutoscaler definitions will be placed, and an HPA template file (`--template`) that specifies HPA parameters except the `metadata/name` and `scaleTargetRef/name` values that will be set as equal to the name of the Deployment found in the input directory. If the output directory is not specified it is equal to the input one.

Examples:
```zsh
python3 Add-on/HPA/create-hpa.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/hpa' --template 'Add-on/HPA/hpa-template.yaml'
```

