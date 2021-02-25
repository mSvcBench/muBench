### #!/usr/bin/python3
import argparse
import json
from json.decoder import JSONDecodeError
import requests
import os
from pathlib import Path
from pprint import pprint
import ServiceMeshGenerator.ServiceMeshGenerator as smGen


'''
gen-servicemesh -o servicemesh.json -v 3 -g 2 -p 2 -e 2 -z 11
'''


# graph_params_test = {"services_groups": 1, "vertices": 10, "power": 1, "edges_per_vertex": 1, "zero_appeal": 10}

def init_args(parser):
    parser.add_argument('-o', action='store', dest='output_file',
                        help='Output File Name', default='servicemesh.json')
    parser.add_argument('-v', action='store', dest='v_number', type=int,
                        help='Vertices Number', default=5)
    parser.add_argument('-g', action='store', dest='services_groups', type=int,
                        help='Number of Services Groups', default=1)
    parser.add_argument('-p', action='store', dest='power', type=int,
                        help='Power of vertices', default=1)
    parser.add_argument('-e', action='store', dest='edge_per_vertex', type=int,
                        help='Number of Edge Per Vertex', default=1)
    parser.add_argument('-z', action='store', dest='zero_appeal', type=int,
                        help='Zero Appeal of vertices', default=10)
    parser.set_defaults(func=run)


def run(args):
    print("Generate ServiceMesh")
    try:
        params = {"services_groups": args.services_groups,
                  "vertices": args.v_number,
                  "power": args.power,
                  "edges_per_vertex": args.edge_per_vertex,
                  "zero_appeal": args.zero_appeal
                  }
        pprint(params)
        output_file = args.output_file
        service_mesh = smGen.get_service_mesh(params)
        with open(output_file, "w") as f:
            f.write(json.dumps(service_mesh))

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
