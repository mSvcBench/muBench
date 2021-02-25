import json
from pprint import pprint
import random

'''    
NEW_work_model
    {'s0': {'params': {'function_1': {'P': 1, 'b': 11, 'c': [101, 101]}}},
     's1': {'params': {'function_3': {'P': 0.6, 'd': 5, 'e': [42, 42]}}},
     's2': {'params': {'function_1': {'P': 1, 'b': 11, 'c': [101, 101]}}},
     's3': {'params': {'function_3': {'P': 0.6, 'd': 5, 'e': [42, 42]}}},
     's4': {'params': {'function_1': {'P': 1, 'b': 11, 'c': [101, 101]}}}}
'''


# Select exactly one job function according to the probability
# Get in INPUT the list with the job functions
def select_job(jobs):
    jobs_items = jobs.items()
    random_extraction = random.random()
    # print("Extraction: %.4f" % random_extraction)
    p_total = 0.0
    for job in jobs.values():
        p_total += job["P"]
    p_total = round(p_total, 10)
    prev_interval = 0
    for job in jobs_items:
        if random_extraction <= prev_interval + job[1]["P"]/p_total:
            return {job[0]: job[1]}
        prev_interval += round(job[1]["P"]/p_total, 10)


def get_work_model(vertex_number, params):
    work_model = dict()
    # pprint(params)
    try:
        for vertex in range(vertex_number):
            work_model[f"s{vertex}"] = {"params": select_job(params)}
    except Exception as err:
        print("ERROR: in creation work model,", err)
        exit(1)

    # pprint(work_model)
    return work_model


# INPUT params:
# v_numbers = 5
# parameters = {"compute_pi": {"P": 1, "b": 11, "c": [101, 101]},
#               "ave_luca": {"P": 0.6, "ave_number": 13, "b": 42}
#               }
#
# # print(select_job(parameters))
# get_work_model(v_numbers, parameters)


# test_dict = {"a": 0.4,
#              "b": 0.3,
#              "c": 0.2,
#              "d": 0.1
#              }
# total = test_dict["a"] + test_dict["b"] + test_dict["c"] + test_dict["d"]
# total_1 = test_dict["a"] + test_dict["d"] + test_dict["c"] + test_dict["b"]
#
#
# if round(total, 10) == total_1:
#     print("VERO")
# else:
#     print("FALSO")



