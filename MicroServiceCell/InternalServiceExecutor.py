import threading
import os
import glob
import random

# Dinamyc import of all function in InternalServiceFunctions folder
for path in glob.glob('MSConfig/InternalServiceFunctions/[!_]*.py'):
    name, ext = os.path.splitext(os.path.basename(path))
    exec(f"from MSConfig.InternalServiceFunctions.{name} import *")


class InternalServiceExecutor(threading.Thread):
    def __init__(self, internal_service_function, params, response):
        threading.Thread.__init__(self)
        self.internal_service_function = f'{internal_service_function}({params})'
        self.response = response

    def run(self):
        # self.internal_service_function()
        self.response.set_body(eval(self.internal_service_function))


class ThreadReturnedValue:
    def __init__(self):
        self.body = None

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body


def compute_pi(params):
    cpu_load = random.randint(params["range_complexity"][0], params["range_complexity"][1])
    pi_greco = list()

    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    counter = 0
    while True:
        if 4 * q + r - t < m * t:
            # yield m
            pi_greco.append(m)
            q, r, t, k, m, x = 10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
            if counter > cpu_load-1:
                break
            else:
                counter = counter+1
        else:
            q, r, t, k, m, x = q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2
    print("Service complexity: %d - Number of cycles for pi computation: %d" % (cpu_load, cpu_load + 1))

    # Make response with size E[Y] = B
    # KB -> 1024**1
    # MB -> 1024**2
    # GB -> 1024**3
    bandwidth_load = random.expovariate(1 / params["mean_bandwidth"])
    print("E[bandwidth] = 1/%d ---> Response size = %d KB" % (params["mean_bandwidth"], bandwidth_load))
    num_chars = 1024 * bandwidth_load  # Response in KB
    response_body = 'L' * int(num_chars)

    return response_body


def run_internal_service(internal_service_params):
    function_name = list(internal_service_params)[0]
    internal_service_params_v = list(internal_service_params.values())[0]
    # response = list()
    # response = dict()
    response = ThreadReturnedValue()
    thread = InternalServiceExecutor(function_name, internal_service_params_v, response)
    thread.start()
    thread.join()
    return response.get_body()


# test_func = {'ave_luca': {'ave_number': 2, 'mean_bandwidth': 42}}
# test_func = {'compute_pi': {'mean_bandwidth': 1, 'range_complexity': [101, 101]}}
# print(run_internal_service(test_func))
