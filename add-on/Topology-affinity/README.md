## create-affinity-yamls

`create-affinity-yamls` is a utility that generates YAML configuration files of Kubernetes deployments that have affinity rules based on the `topology.kubernetes.io/{region,zone,sub-zone}` label of the nodes. 
The software takes as parameters an input directory where there are YAML files without affinity, an output directory where new YAML files with affinity rules will be placed, and the `region`, `zone` and `sub-zone` values to be used in the affinity rules. 
For each combination of `region`, `zone` and `sub-zone` values, the software creates a subdirectory of the output directory that includes the input YAML files whose Deployments have the affinity rules. The names of these deployments are changed into the original name plus the string "-`region`", "-`zone`" and "-`sub-zone`" values. A new `app-t` label equal to the original app one is added to the template labels and matchLabels selector of the Deployment.

Examples:

To create in `SimulationWorkspace/affinity-yamls` a set of YAML files whose Deployments have affinity rules for a region `us-west1`, a zone `us-west1-a`, and a subzone `us-west1-a` from the input directory `SimulationWorkspace/yamls`, the following command can be used:

```zsh
python3 Add-on/Topology-affinity/create-affinity-yamls.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/affinity-yamls' --region 'us-west1' --zone 'us-west1-a'  --subzone 'us-west1-a-a'
```

To create in `SimulationWorkspace/affinity-yamls` a set of YAML files whose Deployments have affinity rules for zone `cloud` and `edge1` from the `SimulationWorkspace/yamls` input directory, the following command can be used:

```zsh
python3 Add-on/Topology-affinity/create-affinity-yamls.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/affinity-yamls' --zone cloud,edge1
```

