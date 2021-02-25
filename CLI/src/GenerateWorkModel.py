### #!/usr/bin/python3
import argparse
import json
from json.decoder import JSONDecodeError
import requests
import os
from pathlib import Path
from pprint import pprint
import WorkModelGenerator.WorkModelGenerator as wmGen


'''
gen-workmodel -o outFile -v 3 -p '{"compute_pi":{"P":1,"b":11,"c":[101,101]},"ave_luca":{"P":0.6,"ave_number":13,"b":42}}'
'''



def init_args(parser):
    parser.add_argument('-o', action='store', dest='output_file',
                        help='Output File Name', default='workmodel.json')
    parser.add_argument('-v', action='store', dest='v_number',
                        help='Vertices Number', default=5)
    parser.add_argument('-p', action='store', dest='params',
                        help='WorkModel parameters', default='{"compute_pi":{"P":1,"b":11,"c":[101,101]}}')
    parser.add_argument('-f', action='store', dest='function_file',
                        help='WorkModel parameters', default='funzioni.json')
    parser.set_defaults(func=run)


def run(args):
    print("Generate WorkModel")
    try:
        v_numbers = args.v_number
        functions = args.function_file
        output_file = args.output_file
        with open(functions) as f:
            parameters = json.load(f)
            # print(parameters)
        #     # asd = json.loads(f.read())

        work_model = wmGen.get_work_model(v_numbers, parameters)
        with open(output_file, "w") as f:
            f.write(json.dumps(work_model))

    except JSONDecodeError as err:
        print("Error: parameters MUST be in json.dumps() format!", err)
        exit()
    except Exception as err:
        print("Error:", err)
        exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    args.func(args)
