import pi
import matrix
import benchmark

import math
import sys

testing = False

elapsed_time = "N/A"
nthreads = int(sys.argv[3])
maxworkers = nthreads


if(testing == True):
    print(pi.compute_pi())
elif (sys.argv[1] == "pi"):
    n_iterations = 1_000_000
    if(sys.argv[2] == "single"):
        elapsed_time = benchmark.count_clocks(f=pi.compute_pi, max_iterations = n_iterations)
        #print(f"no threading: {elapsed_time}")
    elif(sys.argv[2] == "thread"):
        elapsed_time = benchmark.count_clocks(f=pi.compute_pi_thread_pool, n_threads=nthreads, max_workers = maxworkers, max_iterations = n_iterations)
        #print(f"multithreading threadPooling {nthreads} threads: {elapsed_time}")
    elif(sys.argv[2] == "process"):
        elapsed_time = benchmark.count_clocks(f=pi.compute_pi_process_pool, n_threads=nthreads, max_workers = maxworkers, max_iterations = n_iterations)
        #print(f"multithreading processPooling {nthreads} threads: {elapsed_time}")

    #TODO: melhor fazer retorno do script ou fazer ele printar no stdout?
    print(elapsed_time)
elif (sys.argv[1] == "matrix"):
    n = 100
    min_val = -100
    max_val = 100
    seed = 10

    m1 = matrix.get_random_int_matrix(n = n, min_val = min_val, max_val = max_val, seed=seed)
    m2 = matrix.get_random_int_matrix(n = n, min_val = min_val, max_val = max_val, seed=seed+1)

    if(sys.argv[2] == "single"):
        elapsed_time = benchmark.count_clocks(f=matrix.matrix_mult, m1 = m1, m2 = m2)
        #print(f"no threading: {elapsed_time}")
    elif(sys.argv[2] == "thread"):
        elapsed_time = benchmark.count_clocks(f=matrix.matrix_mult_thread_pool, n_threads=nthreads, max_workers = maxworkers, m1=m1, m2=m2)
        #print(f"multithreading threadPooling {nthreads} threads: {elapsed_time}")
    elif(sys.argv[2] == "process"):
        elapsed_time = benchmark.count_clocks(f=matrix.matrix_mult_process_pool, n_threads=nthreads, max_workers = maxworkers, m1=m1, m2=m2)
        #print(f"multithreading processPooling {nthreads} threads: {elapsed_time}")

    #TODO: melhor fazer retorno do script ou fazer ele printar no stdout?
    print(elapsed_time)
