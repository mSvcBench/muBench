#### #!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

import argparse, sys, argcomplete, traceback
sys.path.insert(0, 'src')
# sys.path.insert(0, 'CLI/src')
# sys.path.insert(0, 'MicroServiceSimulator')

sys.path.insert(0, '../')

import GenerateServiceMesh
import GenerateWorkload
import GenerateWorkModel
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar="<command>")

    # generate servicemesh
    parser_sm = subparsers.add_parser('gen-servicemesh', help='Generate WorkModel')
    GenerateServiceMesh.init_args(parser_sm)

    # generate workmodel
    parser_gw = subparsers.add_parser('gen-workmodel', help='Generate WorkModel')
    GenerateWorkModel.init_args(parser_gw)

    # generate workload
    parser_wl = subparsers.add_parser('gen-workload', help='Generate WorkModel')
    GenerateWorkload.init_args(parser_wl)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    try:
        args.func(args)
    except ImportError:
        print("Import error, there are missing dependencies to install.  'apt-get install python3-argcomplete "
              "&& activate-global-python-argcomplete3' may solve")
    except AttributeError:
        parser.print_help()
    except Exception:
        traceback.print_exc()
