from WorkLoadGenerator import get_workload, WORKLOAD_PATH
import json
from pprint import pprint
import sys
import os
import shutil

import argparse
import argcomplete


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The WorkLoad Parameters file', default=f'{WORKLOAD_PATH}/WorkLoadParameters.json')

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


# if len(sys.argv) > 1:
#     parameters_file_path = sys.argv[1]
# elif len(WORKLOAD_PATH) > 0:
#     parameters_file_path = f'{WORKLOAD_PATH}/WorkLoadParameters.json'
# else:
#     parameters_file_path = 'WorkLoadParameters.json'

try:
    with open(parameters_file_path) as f:
        params = json.load(f)
    workload_parameters = params['WorkLoadParameters']
    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = WORKLOAD_PATH

except Exception as err:
    print("ERROR: in RunWorkLoadGen,", err)
    exit(1)


# workload = get_workload(ingress_list, {"min": 1, "max": 3}, request_parameters)
workload = get_workload(workload_parameters)
pprint(workload)
print("# Events: %d" % len(workload))
# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    # with open(f"workload_events_{stop_event}_mean_{mean_interarrival_time}.json", "w") as f:
    with open(f"{output_path}/workload_{workload_parameters['request_parameters']['mean_interarrival_time']}.json", "w") as f:
        f.write(json.dumps(workload, indent=2))

    if output_path != WORKLOAD_PATH:
        shutil.copy(parameters_file_path, f"{output_path}/")

    print(f"'{output_path}/workload_{workload_parameters['request_parameters']['mean_interarrival_time']}.json'")
    print("File Saved!")


