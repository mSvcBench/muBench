import yaml
import os
import argparse

def create_dest_rule(yaml_file_in, yaml_file_out):
    # Function to add node affinity spec for topology.kubernetes.io to a Kubernetes deployment YAML file
    # yaml_file_in: input YAML file 
    # yaml_file_out: output YAML file, whose file contains the affinity spec
    # host: host value

    destrule_template = {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'DestinationRule',
        'metadata':{
        },
        'spec':{
            'trafficPolicy':{
                'connectionPool':{
                    'tcp':{
                        'maxConnections': 1000
                    },
                    'http':{
                        'http2MaxRequests': 1000,
                        'maxRequestsPerConnection': 10
                    },
                },
                'outlierDetection':{
                    'consecutiveErrors': 7,
                    'interval': '30s',
                    'baseEjectionTime': '30s'
                }
            }
        }
    }

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
# python3 add-on/edge-computing/create-affinity-yamls.py --in 'SimulationWorkspace/yamls' --out 'add-on/edge-computing/dest-rule-yamls' 

def main():
    parser = argparse.ArgumentParser(description='Create destination rules enabling istio locality load balancing for Kubernetes services')
    parser.add_argument('--in', type=str, help='Path of the input YAML files',action='store', dest='yaml_file_in_path',default='SimulationWorkspace/yamls')
    parser.add_argument('--out', type=str, help='Path of the output YAML files',action='store', dest='yaml_file_out_path',default='add-on/edge-computing/dest-rule-yamls')
    
    args = parser.parse_args()
    
    yaml_file_in_path = args.yaml_file_in_path
    yaml_file_out_path = args.yaml_file_out_path
    os.makedirs(yaml_file_out_path, exist_ok=True)

    for filename in os.listdir(yaml_file_in_path):
        if filename.endswith(".yaml"):
            yaml_file_out = os.path.join(yaml_file_out_path, 'dest_rule-'+filename)
            yaml_file_in = os.path.join(yaml_file_in_path, filename)
            create_dest_rule(yaml_file_in, yaml_file_out)
            print(f"Created dest rule yaml file: {yaml_file_out}")

if __name__ == "__main__":
    main()