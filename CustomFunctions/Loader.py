import random
import time
import os
from concurrent.futures import ThreadPoolExecutor, wait
import jsonmerge
import string

params_processed = False
params = dict()

def cpu_loader_job(params):
    cpu_load = random.randint(params["range_complexity"][0], params["range_complexity"][1])
    trials = int(params["trials"])

    for x in range(trials):
        pi_greco = list()
        q, r, t, k, m, x = 1, 0, 1, 1, 3, 3
        counter = 0
        while True:
            if 4 * q + r - t < m * t:
                # yield m
                pi_greco.append(str(m))
                q, r, t, k, m, x = 10*q, 10*(r-m*t), t, k, (10*(3*q+r))//t - 10*m, x
                if counter > cpu_load-1:
                    break
                else:
                    counter = counter+1
            else:
                q, r, t, k, m, x = q*k, (2*q+r)*x, t*x, k+1, (q*(7*k+2)+r*x)//(t*x), x+2
        #print("Service complexity: %d - Number of cycles for pi computation: %d" % (cpu_load, cpu_load + 1))
        # print(f"Value: 3.{''.join(pi_greco[1:])}\n")

def cpu_loader(params):
    # print("--------> CPU stress start")
    pool_size = int(params["thread_pool_size"])
    pool = ThreadPoolExecutor(pool_size)
    futures = list()
    for thread in range(pool_size):
        futures.append(pool.submit(cpu_loader_job, params))
    wait(futures)
    # print("--------> CPU stress test stop")
    return

def bandwidth_loader(params):
    # print("--------> Network stress start")
    bandwidth_load = random.expovariate(1 / params["mean_response_size"])
    num_chars = int(max(1, 1000 * bandwidth_load))  # Response in kB
    response_body = ''.join(random.choice(string.ascii_letters) for i in range(num_chars))
    # print("--------> Network stress stop")
    return response_body

def memory_loader(params):
    # print("--------> Memory stress start")
    memory_size = params["memory_size"]
    memory_io = params["memory_io"]
    
    # allocate memory_size kB of memory
    dummy_buffer = []
    dummy_buffer = ['A' * 1000 for _ in range(0, int(memory_size))]
    
    for i in range(0, int(memory_io)):
        v = dummy_buffer[i % int(memory_size)]  # read operation
        dummy_buffer[i % int(memory_size)] = ['A' * 1000] # write operation
    # print("--------> Memory stress stop")
    return dummy_buffer

def disk_loader(params):
        # print("--------> Disk stress start")
        # print("--------> Write stress start")
        filename_base = params["tmp_file_name"]
        rnd_str = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        filename = f"{rnd_str}-{filename_base}"
        blocks_count = params["disk_write_block_count"]
        block_size = params["disk_write_block_size"]
        f = os.open(filename, os.O_CREAT | os.O_WRONLY, 0o777)  # low-level I/O
        for i in range(blocks_count):
            buff = os.urandom(block_size)
            os.write(f, buff)
        os.fsync(f)  # force write to disk
        os.close(f)
        # print("--------> Write stress stop")

        # print("--------> Read stress start")
        f = os.open(filename, os.O_RDONLY, 0o777)  # low-level I/O
        # generate random read positions
        offsets = list(range(0, blocks_count * block_size, block_size))
        random.shuffle(offsets)

        for i, offset in enumerate(offsets, 1):
            os.lseek(f, offset, os.SEEK_SET)  # set position
            buff = os.read(f, block_size)  # read from position
            if not buff: break  # if EOF reached
        os.close(f)
        # print("--------> Read stress stop")
        os.remove(filename)
        return

def sleep_loader(params):
    # print("--------> Sleep start")
    time.sleep(float(params["sleep_time"]))
    # print("--------> Sleep stop")
    return

def loader(input_params):
    global params_processed, params

    if not params_processed:
        default_params = {
            "cpu_stress": {"run":False,"range_complexity": [100, 100], "thread_pool_size": 1, "trials": 1},
            "memory_stress":{"run":False, "memory_size": 10000, "memory_io": 1000},
            "disk_stress":{"run":False,"tmp_file_name":  "mubtestfile.txt", "disk_write_block_count": 1000, "disk_write_block_size": 1024},
            "sleep_stress":{"run":True,"sleep_time": 0.01},
            "mean_response_size": 11}

        params = jsonmerge.merge(default_params,input_params)
        if "mean_bandwidth" in params:
            # for backward compatibility
            params["mean_response_size"] = params["mean_bandwidth"]
        params_processed = True    
    if params['cpu_stress']['run']: 
        cpu_loader(params['cpu_stress'])
    if params['memory_stress']['run']:
        memory_loader(params['memory_stress'])
    if params['disk_stress']['run']:
        disk_loader(params['disk_stress'])
    if params['sleep_stress']['run']:
        sleep_loader(params['sleep_stress'])
    return bandwidth_loader(params)

if __name__ == '__main__':
    loader({})