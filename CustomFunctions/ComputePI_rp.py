# This function computes X decimal points of pi,
# where X is a random integer in range_complexity[0] and range_complexity[1].
# The evaluation is repeated parallelly trials times with thread_pool_size number of threads

import random
import time
from concurrent.futures import ThreadPoolExecutor, wait


def compute_pi_job(params):
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


def compute_pi_r_job(params):
    cpu_load = random.randint(params["range_complexity"][0], params["range_complexity"][1])
    trials = int(params["trials"])

    for x in range(trials):
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


def compute_pi_rp(params):
    pool_size = int(params["thread_pool_size"])
    pool = ThreadPoolExecutor(pool_size)
    futures = list()
    for thread in range(pool_size):
        futures.append(pool.submit(compute_pi_r_job, params))

    wait(futures)
    print("--------> Threads Done!")

    # Make response with size E[Y] = B
    # KB -> 1024**1
    # MB -> 1024**2
    # GB -> 1024**3
    bandwidth_load = random.expovariate(1 / params["mean_bandwidth"])
    print("E[bandwidth] = 1/%d ---> Response size = %d KB" % (params["mean_bandwidth"], bandwidth_load))
    num_chars = 1024 * bandwidth_load  # Response in KB
    response_body = 'L' * int(num_chars)
    return response_body


# prams = {"mean_bandwidth": 11, "range_complexity": [101, 101], "trials": 10, "thread_pool_size": 5}
# compute_pi_rp(prams)


