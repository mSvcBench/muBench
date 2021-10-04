from TrafficGenerator import get_Traffic, Traffic_PATH
import json
from pprint import pprint
import sys
import os
import shutil

import argparse
import argcomplete

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config-file', action='store', dest='parameters_file',
                    help='The Traffic Parameters file', default=f'{Traffic_PATH}/TrafficParameters.json')

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
    Traffic_parameters = params['TrafficParameters']
    if "OutputPath" in params.keys() and len(params["OutputPath"]) > 0:
        output_path = params["OutputPath"]
        if output_path.endswith("/"):
            output_path = output_path[:-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    else:
        output_path = Traffic_PATH
    if "OutputFile" in params.keys() and len(params["OutputFile"]) > 0:
        output_file = params["OutputFile"]
    else:
        output_file = "workload.json"

except Exception as err:
    print("ERROR: in RunTrafficGen,", err)
    exit(1)

Traffic = get_Traffic(Traffic_parameters)
pprint(Traffic)
print("# Events: %d" % len(Traffic))
# keyboard_input = input("Save work model on file? (y)") or "y"
keyboard_input = "y"

if keyboard_input == "y":
    with open(f"{output_path}/{output_file}", "w") as f:
        f.write(json.dumps(Traffic, indent=2))

    #if output_path != Traffic_PATH:
    #    shutil.copy(parameters_file_path, f"{output_path}/")

    print(f"'{output_path}/{output_file}")
    print("File Saved!")


