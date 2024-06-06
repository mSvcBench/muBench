import sys
import os
import argparse
import argcomplete
import json

AUTOPILOT_PATH = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The Autopilot Parameters file', default=f'{AUTOPILOT_PATH}/K8sAutopilotConf.json')

argcomplete.autocomplete(parser)

try:
    args = parser.parse_args()
except ImportError:
    print("Import error, there are missing dependencies to install.  'apt-get install python3-argcomplete "
          "&& activate-global-python-argcomplete3' may solve")
except AttributeError:
    parser.print_help()
except Exception as err:
    print("Error:", err)


parameters_file_path = args.parameters_file
try:
    with open(parameters_file_path) as f:
        params = json.load(f)

    ##### ServiceGraph Params
    graph_run = params['RunServiceGraphGeneratorFilePath']
    graph_parameters = params['ServiceGraphParametersFilePath']
    ##### WorkModel Params
    workmodel_run = params['RunWorkModelGeneratorFilePath']
    workmodel_parameters = params['WorkModelParametersFilePath']
    #### K8s Deployer
    k8s_run = params['RunK8sDeployerFilePath']
    k8s_parameters = params['K8sParametersFilePath']

except Exception as err:
    print("ERROR: in config file,", err)
    exit(1)

os.system('python3 '+f'{graph_run} -c {graph_parameters}')
os.system('python3 '+f'{workmodel_run} -c {workmodel_parameters}')
os.system('python3 '+f'{k8s_run} -c {k8s_parameters}')

