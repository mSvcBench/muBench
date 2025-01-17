import yaml
import os
import argparse

def create_hpa(yaml_file_in, yaml_file_out, hpa_template_file):
    # Function to create an Horizontal Pod Autoscaler for Kubernetes service
    with open(hpa_template_file, 'r') as template_file:
        hpa_template = yaml.safe_load(template_file)
    with open(yaml_file_in, 'r') as file:
        complete_yaml = list(yaml.safe_load_all(file))
    for partial_yaml in complete_yaml:
        if partial_yaml["kind"] == "Deployment":
            if 'metadata' not in partial_yaml or 'name' not in partial_yaml['metadata']:
                raise ValueError('Invalid Kubernetes Service YAML')
            else:
                hpa=hpa_template.copy()
                hpa['metadata']['name'] = partial_yaml['metadata']['name']
                hpa['spec']['scaleTargetRef']['name'] = partial_yaml['metadata']['name']
                if 'namespace' in partial_yaml['metadata']:
                    hpa['metadata']['namespace'] = partial_yaml['metadata']['namespace']
                with open(yaml_file_out, 'w') as file:
                    yaml.dump(hpa, file, default_flow_style=False)
                    print(f"Created HPA yaml file: {yaml_file_out}")

# Example usage:
# python3 Add-on/HPA/create-hpa.py --in 'SimulationWorkspace/yamls' --out 'SimulationWorkspace/hpa' --template 'Add-on/HPA/hpa-template.yaml' 

def main():
    parser = argparse.ArgumentParser(description='Create destination rules enabling istio locality load balancing for Kubernetes services')
    parser.add_argument('--in', type=str, help='Path of the input YAML files',action='store', dest='yaml_file_in_path',default='SimulationWorkspace/yamls')
    parser.add_argument('--out', type=str, help='Path of the output YAML files',action='store', dest='yaml_file_out_path',default='not-defined')
    parser.add_argument('--template', type=str, help='Path of the HPA YAML file template',action='store', dest='hpa_template_file',default='Add-on/HPA/hpa-template.yaml')
    
    args = parser.parse_args()
    
    yaml_file_in_path = args.yaml_file_in_path
    yaml_file_out_path = args.yaml_file_out_path
    if yaml_file_out_path == 'not-defined':
        yaml_file_out_path = yaml_file_in_path
    os.makedirs(yaml_file_out_path, exist_ok=True)

    for filename in os.listdir(yaml_file_in_path):
        if filename.endswith(".yaml"):
            yaml_file_out = os.path.join(yaml_file_out_path, 'hpa-'+filename)
            yaml_file_in = os.path.join(yaml_file_in_path, filename)
            create_hpa(yaml_file_in, yaml_file_out,hpa_template_file=args.hpa_template_file)

if __name__ == "__main__":
    main()