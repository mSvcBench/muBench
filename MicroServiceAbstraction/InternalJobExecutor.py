import threading
import time


class InternalJobExecutor(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self)
        self.params = params

    def run(self):
        self.internal_job()

    def internal_job(self):
        print("PERDO TEMPO ESEGUENDO INTERNAL JOB, T: %s, B: %s" % (self.params["T"], self.params["B"]))
        time.sleep(8)
        print("SONO PASSATI 8 SECONDI")


def cpu_test():
    plus_minus = False
    pi = 0.0
    # Serie infinita π = (4/1)-(4/3)+(4/5)-(4/7)+(4/9)-(4/11)+(4/13)-(4/15) ...
    for i in range(1, 100000, 2):
        if plus_minus:
            pi -= 4.0 / i
            plus_minus = False
            print(pi)
        else:
            pi += 4.0 / i
            plus_minus = True
            print(pi)

    print(pi)


def run_internal_job(job_params):
    thread = InternalJobExecutor(job_params)
    thread.start()
    thread.join()



