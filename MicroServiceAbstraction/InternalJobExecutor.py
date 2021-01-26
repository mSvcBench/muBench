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
        print("PERDO TEMPO ESEGUENDO INTERNAL JOB, E[Xtempo]= %s, E[Ybanda]= %s" % (self.params["T"], self.params["B"]))
        # Negative Exponential Distribution with E[X] = 1/λ, T = 1/λ -> E[X] = T
        cpu_load = random.expovariate(1/int(self.params["T"]))
        finish_time = datetime.now() + timedelta(milliseconds=cpu_load)
        cnt = 0
        while datetime.now() < finish_time:
            cnt += 1
            cpu_test()
        print("Number of cycles %d" % cnt)

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



