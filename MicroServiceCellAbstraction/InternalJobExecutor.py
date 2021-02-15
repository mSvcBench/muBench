import threading
from JobFunctions import *
from pprint import pprint


class InternalJobExecutor(threading.Thread):
    def __init__(self, job_function, params, response):
        threading.Thread.__init__(self)
        self.job_function = f'{job_function}(%s)'
        self.params = params
        self.response = response

    def run(self):
        self.internal_job()

    def internal_job(self):
        self.response.set_body(eval(self.job_function % self.params))
        # self.response.append(eval(self.job_function % self.params)[0])
        # self.response = eval(self.job_function % self.params)[0]


class ThreadReturnedValue:
    def __init__(self):
        self.body = None

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body


def compute_pi(params):
    cpu_load = random.randint(params["c"][0], params["c"][1])
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
    print("Job complexity: %d - Number of cycles for pi computation: %d" % (cpu_load, cpu_load + 1))

    # Make response with size E[Y] = B
    # KB -> 1024**1
    # MB -> 1024**2
    # GB -> 1024**3
    bandwidth_load = random.expovariate(1 / params["b"])
    print("E[bandwidth] = 1/%d ---> Response size = %d KB" % (params["b"], bandwidth_load))
    num_chars = 1024 * bandwidth_load  # Response in KB
    response_body = 'L' * int(num_chars)

    return response_body


def run_internal_job(job_params):
    function_name = list(job_params)[0]
    job_params_v = list(job_params.values())[0]
    # response = list()
    # response = dict()
    response = ThreadReturnedValue()
    thread = InternalJobExecutor(function_name, job_params_v, response)
    thread.start()
    thread.join()
    return response.get_body()


# asd = run_internal_job({'compute_pi': {'P': 1, 'b': 1, 'c': [101, 101]}})
# pprint(asd)
# pprint(len(asd))
# run_internal_job({'say_hello_to_luca': {"hellos_number": 13, "b": 42}})
