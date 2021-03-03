import json
from pprint import pprint
import random

# Select exactly one job function according to the probability
# Get in INPUT the list with the job functions
def select_job(jobs):
    jobs_items = jobs.items()
    random_extraction = random.random()
    # print("Extraction: %.4f" % random_extraction)
    p_total = 0.0
    for job in jobs.values():
        p_total += job["probability"]
    p_total = round(p_total, 10)
    prev_interval = 0
    for job in jobs_items:
        if random_extraction <= prev_interval + job[1]["probability"]/p_total:
            tmp_param = dict(job[1])
            tmp_param.pop("probability")
            return {job[0]: tmp_param}
        prev_interval += round(job[1]["probability"]/p_total, 10)


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
    print("Work Model Created!")
    return work_model


# INPUT params:
# v_numbers = 5
# parameters = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [101, 101]},
#               "ave_luca": {"probability": 0.6, "ave_number": 13, "mean_bandwidth": 42}
#               }
#
# print(select_job(parameters))
# pprint(get_work_model(v_numbers, parameters))


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



