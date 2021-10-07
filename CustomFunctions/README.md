# Description of Custom Internal Functions

## Colosseum

Function that returns a simple asci art of Colosseum

*Function name* : `colosseum`

*Input Paramenters* : none

## ComputePI

This *single-thread* internal function (included in the service-cell code) stresses the CPU by computing `D` decimal points of pi, where `D` is a random integer in `range_complexity` (e.g. 50,100). The return is a string whose length is a sample of an exp neg random variable with mean `mean_bandwidth` kBytes  

*Function name* : `compute_pi`

*Default Input Paramenters* :

```json
{
    "range_complexity": [50, 100], 
    "mean_bandwidth": 10
}
```

## Loader

This *multi-thread* internal function sequentially load the CPU, the memory, and the disk. 

The CPU stress is performed (if `run`=true) by running `thread_pool_size` parallel jobs. Each job computes `D` decimal points of pi, where `D` is a random integer in `range_complexity` (e.g. 50,100). The computation is repeated sequentially `trials` times per job.

The memory stress is performed (if `run`=true) by allocating `mean_memory_size` kBytes. Then `mean_memory_io` read/write operations of 1 byte are executed sequentially.

The disk stress is performed by creating the file `tmp_file_name`. Writing `disk_write_block_count` blocks of  `disk_write_block_size` bytes. Finally, random accessing each of them once.

The return is a string whose length is a sample of an exp neg random variable with mean `mean_bandwidth` kBytes.

*Function name* : `loader`

*Default Input Paramenters* :

```json
{
        "cpu_stress": {
            "run":true,
            "range_complexity": [100, 100], "thread_pool_size": 1, 
            "trials": 1
        },
        "memory_stress":{
            "run":true, 
            "mean_memory_size": 10000, "mean_memory_io": 1000
        },
        "disk_stress":{
            "run":true,
            "tmp_file_name":  "mubtestfile.txt", 
            "disk_write_block_count": 1000, "disk_write_block_size": 1024
        },
        "mean_bandwidth": 11}
```