import json
from pprint import pprint
import random

'''
work_model
    {
    "s1": {"params": {"c": 101, "b": 11}},
    "s2": {"params": {"c": 102, "b": 12}},
    "s3": {"params": {"c": 103, "b": 13}},
    "s4": {"params": {"c": 104, "b": 14}},
    "s5": {"params": {"c": 105, "b": 15}}
    }
    
    
NEW_work_model
    {'s0': {'params': {'function_1': {'P': 1, 'b': [11, 11], 'c': [101, 101]}}},
     's1': {'params': {'function_3': {'P': 0.6, 'd': [5, 5], 'e': [42, 42]}}},
     's2': {'params': {'function_1': {'P': 1, 'b': [11, 11], 'c': [101, 101]}}},
     's3': {'params': {'function_3': {'P': 0.6, 'd': [5, 5], 'e': [42, 42]}}},
     's4': {'params': {'function_1': {'P': 1, 'b': [11, 11], 'c': [101, 101]}}}}
'''


# Select exactly one job function according to the probability
# Get in INPUT the list with the job functions
def select_job(jobs):
    jobs_items = jobs.items()
    random_extraction = random.random()
    # random_extraction = 0.2
    # print("Extraction: %.4f" % random_extraction)
    selected_job = None
    for job in jobs_items:
        if random_extraction <= job[1]["P"] and selected_job is None:
            selected_job = job
            continue

        if random_extraction <= job[1]["P"] < selected_job[1]["P"]:
            selected_job = job

    if selected_job is None:
        print("Error: The default job Function must have probability values (P) set to 1")
        exit()
    else:
        return {selected_job[0]: selected_job[1]}


def get_work_model(vertex_number, params):
    work_model = dict()
    # pprint(params)
    try:
        for vertex in range(vertex_number):
            work_model[f"s{vertex}"] = {"params": select_job(params)}
    except Exception as err:
        print("ERROR: in creation work model,", err)
        exit(1)

    pprint(work_model)
    return work_model


def OLD_get_work_model(vertex_number, params):
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


# INPUT params:
v_numbers = 5
parameters = {"compute_pi": {"P": 1, "b": 11, "c": [101, 101]},
              "ave_luca": {"P": 0.6, "ave_number": 13, "b": 42}
              }

get_work_model(v_numbers, parameters)

# print(select_job(parameters))

# OLD_get_work_model(10, {"b": [2, 2], "c": [1, 1]})
