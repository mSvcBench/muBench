import threading
import time
import random
from datetime import datetime, timedelta

MAX_ITERATION = 1000

class InternalJobExecutor(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self)
        self.params = params

    def run(self):
        self.internal_job()

    def internal_job(self):
        print("JOB: complexity = %s" % self.params["c"])
        cpu_load = self.params["c"]
        cnt = 0
        for i in compute_pi(cpu_load):
            cnt += 1
        print("Number of cycles for pi computation: %d" % cnt)


def compute_pi(n):
    q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
    counter = 0
    while True:
        if 4 * q + r - t < m * t:
            yield m
            q, r, t, k, m, x = 10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
            if counter > n-1:
                break
            else:
                counter = counter+1
        else:
            q, r, t, k, m, x = q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2


def cpu_test():
    plus_minus = False
    pi = 0.0
    # Serie infinita π = (4/1)-(4/3)+(4/5)-(4/7)+(4/9)-(4/11)+(4/13)-(4/15) ...
    for i in range(1, MAX_ITERATION, 2):
        if plus_minus:
            pi -= 4.0 / i
            plus_minus = False
            # print(pi)
        else:
            pi += 4.0 / i
            plus_minus = True
            # print(pi)

    # print(pi)


def run_internal_job(job_params):
    thread = InternalJobExecutor(job_params)
    thread.start()
    thread.join()

