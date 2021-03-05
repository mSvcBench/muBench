from WorkModelGenerator import get_work_model, pprint, json

# INPUT params:
v_numbers = 5
parameters = {"compute_pi": {"probability": 1, "mean_bandwidth": 11, "range_complexity": [101, 101]},
              "ave_luca": {"probability": 0.6, "ave_number": 13, "mean_bandwidth": 42}
              }

####################


workmodel = get_work_model(v_numbers, parameters)
pprint(workmodel)

keyboard_input = input("Save work model on file? (y)") or "y"

if keyboard_input == "y":
    with open("workmodel.json", "w") as f:
        f.write(json.dumps(workmodel))
