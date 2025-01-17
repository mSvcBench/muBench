import yaml
import os
import argparse

def add_affinity_spec(yaml_file_in, yaml_file_out, region, zone, subzone ):
    # Function to add node affinity spec for topology.kubernetes.io to a Kubernetes deployment YAML file
    # yaml_file_in: input YAML file 
    # yaml_file_out: output YAML file, whose file contains the affinity spec
    # region: region value
    # zone: zone value
    # subzone: sub-zone value

    suffix=''
    affinity = {
        'nodeAffinity': {
            'requiredDuringSchedulingIgnoredDuringExecution': {
                'nodeSelectorTerms': [{
                    'matchExpressions': []
                }]
            }
        }
    }
    if region != 'no-region-specified':
        affinity['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']['nodeSelectorTerms'][0]['matchExpressions'].append({
            'key': 'topology.kubernetes.io/region',
            'operator': 'In',
            'values': [region]
        })
        suffix=suffix+'-'+region
    if zone != 'no-zone-specified':
        affinity['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']['nodeSelectorTerms'][0]['matchExpressions'].append({
            'key': 'topology.kubernetes.io/zone',
            'operator': 'In',
            'values': [zone]
        })
        suffix=suffix+'-'+zone
    if subzone != 'no-subzone-specified':
        affinity['nodeAffinity']['requiredDuringSchedulingIgnoredDuringExecution']['nodeSelectorTerms'][0]['matchExpressions'].append({
            'key': 'topology.kubernetes.io/subzone',
            'operator': 'In',
            'values': [subzone]
        })
        suffix=suffix+'-'+subzone

    created=False
    with open(yaml_file_in, 'r') as file:
        complete_yaml = list(yaml.safe_load_all(file))
    for partial_yaml in complete_yaml:
        if partial_yaml["kind"] == "Deployment":
            if 'spec' not in partial_yaml or 'template' not in partial_yaml['spec'] or 'spec' not in partial_yaml['spec']['template']:
                raise ValueError('Invalid Kubernetes deployment YAML')
            else:
                if suffix != '':
                    partial_yaml['spec']['template']['spec']['affinity'] = affinity
                    partial_yaml['metadata']['name'] = partial_yaml['metadata']['name'] + suffix
                    partial_yaml['spec']['selector']['matchLabels']['app-t'] = partial_yaml['spec']['selector']['matchLabels']['app'] + suffix
                    partial_yaml['spec']['template']['metadata']['labels']['app-t'] = partial_yaml['spec']['selector']['matchLabels']['app'] + suffix
                    created = created or True
    
    with open(yaml_file_out, 'w') as file:
        yaml.dump_all(complete_yaml, file,default_flow_style=False)
    if created:
        print(f"Created affinity yaml file: {yaml_file_out}")
    else:
        print(f"Copyed yaml file: {yaml_file_out}")
        

def list_of_strings(arg):
    return arg.split(',')

# Example usage:
# python3 Add-on/Topology-affinity/create-affinity-yamls.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/affinity-yamls' --region 'us-west1' --zone 'us-west1-a'  --subzone 'us-west1-a-a'
# python3 Add-on/Topology-affinity/create-affinity-yamls.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/affinity-yamls' --zone cloud,edge1
def main():
    parser = argparse.ArgumentParser(description='Add node affinity spec for zone, region and sub-zone to Kubernetes deployments')
    parser.add_argument('--in', type=str, help='Path of the input YAML files',action='store', dest='yaml_file_in_path',default='SimulationWorkspace/yamls')
    parser.add_argument('--out', type=str, help='Path of the output YAML files',action='store', dest='yaml_file_out_path',default='SimulationWorkspace/affinity-yamls')
    parser.add_argument('--regions', type=list_of_strings, help='list of region values',action='store', dest='regions',default=['no-region-specified'])
    parser.add_argument('--zones', type=list_of_strings, help='list of zone values',action='store', dest='zones',default=['no-zone-specified'])
    parser.add_argument('--subzones', type=list_of_strings, help='list of sub-zone values',action='store', dest='subzones',default=['no-subzone-specified'])
    args = parser.parse_args()
    
    yaml_file_in_path = args.yaml_file_in_path
    yaml_file_out_path = args.yaml_file_out_path
    region_values = args.regions
    zone_values = args.zones
    subzone_values = args.subzones
    os.makedirs(yaml_file_out_path, exist_ok=True)
    
    # create directory structure for region, zone and sub-zone
    for region in region_values:
            os.makedirs(os.path.join(yaml_file_out_path, region), exist_ok=True)
            for zone in zone_values:
                os.makedirs(os.path.join(yaml_file_out_path, region+'/'+zone), exist_ok=True)
                for subzone in subzone_values:
                    os.makedirs(os.path.join(yaml_file_out_path, region+'/'+zone+'/'+subzone), exist_ok=True)
    
    for filename in os.listdir(yaml_file_in_path):
        if filename.endswith(".yaml"):
            yaml_file_in = os.path.join(yaml_file_in_path, filename)
            for region in region_values:
                for zone in zone_values:
                    for subzone in subzone_values:
                        yaml_file_out = os.path.join(yaml_file_out_path+'/'+region+'/'+zone+'/'+subzone, filename)
                        add_affinity_spec(yaml_file_in, yaml_file_out, region, zone, subzone)

if __name__ == "__main__":
    main()