import yaml
import os
import argparse

def create_dest_rule(yaml_file_in, yaml_file_out, dest_rule_template):
    # Function to add node affinity spec for topology.kubernetes.io to a Kubernetes deployment YAML file
    # yaml_file_in: input YAML file 
    # yaml_file_out: output YAML file, whose file contains the affinity spec
    # host: host value

    with open(dest_rule_template, 'r') as template_file:
        destrule_template = yaml.safe_load(template_file)

    with open(yaml_file_in, 'r') as file:
        complete_yaml = list(yaml.safe_load_all(file))
    for partial_yaml in complete_yaml:
        if partial_yaml["kind"] == "Service":
            if 'metadata' not in partial_yaml or 'name' not in partial_yaml['metadata']:
                raise ValueError('Invalid Kubernetes Service YAML')
            else:
                destrule=destrule_template.copy()
                destrule['metadata']['name'] = partial_yaml['metadata']['name']
                destrule['spec']['host'] = partial_yaml['metadata']['name']
                if 'namespace' in partial_yaml['metadata']:
                    destrule['metadata']['namespace'] = partial_yaml['metadata']['namespace']
                with open(yaml_file_out, 'w') as file:
                    yaml.dump(destrule, file,default_flow_style=False)

# Example usage:
# python3 add-on/edge-computing/create-destination-rule.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/dest-rule-yamls' --template 'add-on/edge-computing/destination-rule-template.yaml' 

def main():
    parser = argparse.ArgumentParser(description='Create destination rules enabling istio locality load balancing for Kubernetes services')
    parser.add_argument('--in', type=str, help='Path of the input YAML files',action='store', dest='yaml_file_in_path',default='SimulationWorkspace/yamls')
    parser.add_argument('--out', type=str, help='Path of the output YAML files',action='store', dest='yaml_file_out_path',default='SimulationWorkspace/dest-rule-yamls')
    parser.add_argument('--template', type=str, help='Path of the Destination Rule YAML file template',action='store', dest='dest_rule_template',default='add-on/edge-computing/destination-rule-template.yaml')
    
    args = parser.parse_args()
    
    yaml_file_in_path = args.yaml_file_in_path
    yaml_file_out_path = args.yaml_file_out_path
    os.makedirs(yaml_file_out_path, exist_ok=True)

    for filename in os.listdir(yaml_file_in_path):
        if filename.endswith(".yaml"):
            yaml_file_out = os.path.join(yaml_file_out_path, filename)
            yaml_file_in = os.path.join(yaml_file_in_path, filename)
            create_dest_rule(yaml_file_in, yaml_file_out,dest_rule_template=args.dest_rule_template)
            print(f"Created dest rule yaml file: {yaml_file_out}")

if __name__ == "__main__":
    main()