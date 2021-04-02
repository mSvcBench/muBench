from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import sched
import time
from TimingError import TimingError
import requests
import json
from pprint import pprint
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

# ms_access_gateway = "http://localhost:9999"
# ms_access_gateway = "http://n1:31113"
ms_access_gateway = "http://51.144.151.90:31113"
# ms_access_gateway = "http://vm1:31113"
workload_file_path = "../WorkLoadGenerator/workload.json"
start_time = 0.0


def do_requests(event):
    # pprint(workload[event]["services"])
    for services in event["services"]:
        # print(services)
        try:
            r = requests.get(f"{ms_access_gateway}/{services}")
            delta_diff = r.elapsed.total_seconds()
            # print(f"DELAY DIFF >> {delta_diff}")
            # print(r)
            return event['time'], delta_diff
        except Exception as err:
            print("Error: %s" % err)


def job_assignment(v_pool, v_futures, event):
    try:
        worker = (v_pool.submit(do_requests, event))
        time.sleep(0.0001)  # lascia il tempo di cambiare la variabile _state
        # print(f"{v_time}-{worker._state}-{time.time()}")
        # print(f"{event['time']} - {worker._state} - Delay: {time.time()/1000-start_time-event['time']}")
        # Se il thread viene messo in pending significa che non ho thread liberi e quindi non rispetto
        # i tempi per le richieste
        if worker._state == "PENDING":
            raise TimingError(event['time'])
        v_futures.append(worker)
    except TimingError as err:
        print("Error: %s" % err)


def runner():
    global start_time
    print("I am THE Runner!!")
    with open(workload_file_path) as f:
        workload = json.load(f)
    # pprint(workload)
    # pprint(work_model)
    s = sched.scheduler(time.time, time.sleep)
    pool = ThreadPoolExecutor(320)
    futures = list()
    # print("Time_1:", time.time()*1000)
    # events = [10, 20, 30, 40, 50, 100, 150]
    # events = [0, 1, 2, 3, 4, 5, 10, 15]
    # for event_time in events:
    for event in workload:
        # s.enter(event_time, 1, job_assignment, argument=(pool, futures, event_time))
        # in seconds
        # s.enter(event["time"], 1, job_assignment, argument=(pool, futures, event))
        # in milliseconds
        s.enter(event["time"]/1000, 1, job_assignment, argument=(pool, futures, event))


    start_time = time.time()
    print("Time_1:", start_time)
    s.run()

    wait(futures)
    # plot_list = list()
    # for x in as_completed(futures):
    #     plot_list.append([x.result()[0], x.result()[1]])
        # print(f"{x.result()[0]} ----> {x.result()[1]}")

    # plot_list = sorted(plot_list, key=lambda l: l[0])
    # #print(plot_list)
    #
    # t = []
    # d = []
    # # Data for plotting
    # for element in plot_list:
    #     t.append(element[0])
    #     d.append(element[1])
    #
    # fig, ax = plt.subplots()
    # ax.plot(t, d)
    #
    # ax.set(xlabel='time step', ylabel='delay (ms)',
    #        title='Delay plot')
    # ax.grid()
    # plt.ylim(0, 2)
    #
    # fig.savefig("test2.png")
    # plt.show()


runner()
