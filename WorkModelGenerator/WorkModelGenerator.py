import json
from pprint import pprint
import random

'''
service_model
    {
    "s1": {"params": {"c": 101, "b": 11}},
    "s2": {"params": {"c": 102, "b": 12}},
    "s3": {"params": {"c": 103, "b": 13}},
    "s4": {"params": {"c": 104, "b": 14}},
    "s5": {"params": {"c": 105, "b": 15}}
    }
'''


def get_work_model(vertex_number, params):
    work_model = dict()
    try:
        for vertex in range(vertex_number):
            work_model[f"s{vertex}"] = {"c": random.randint(params["c"][0], params["c"][1]),
                                        "b": random.randint(params["b"][0], params["b"][1])}
    except Exception as err:
        print("ERROR: in creation work model,", err)
        exit(1)

    pprint(work_model)
    return work_model


get_work_model(10, {"b": [2, 2], "c": [1, 1]})
