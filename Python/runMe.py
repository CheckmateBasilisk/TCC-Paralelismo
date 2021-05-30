import pi
import matrix
import benchmark
import math

testing = True

runpi = False
runmatrix = False

if(runpi == True):
    progress_bar = True
    elapsed_time = "N/A"

    # COMPUTING PI
    n_iterations = 1_000_000

    # getting the elapsed time of 1 run, using 10m iterations
    elapsed_time = benchmark.count_clocks(f = pi.compute_pi, max_iterations = n_iterations)
    print(f"1 run: {elapsed_time}")

    # getting the elapsed time of 30 runs, no threading
    n_runs = 30
    elapsed_time = benchmark.avg_count_clocks(progress_bar = progress_bar, f=pi.compute_pi, n_runs=n_runs, max_iterations = n_iterations)
    print(f"avg of {n_runs} (no threading): {elapsed_time}")

    # getting the elapsed time of 30 runs, using multithreading through threadPooling (max_workers = nthreads)
    nthreads = 4
    maxworkers = nthreads
    elapsed_time = benchmark.avg_count_clocks(progress_bar = progress_bar, f=pi.compute_pi_thread_pool, n_runs=n_runs, n_threads=nthreads, max_workers = maxworkers, max_iterations = n_iterations)
    print(f"avg of {n_runs} (multithreading threadPooling {nthreads} threads): {elapsed_time}")

    # getting the elapsed time of 30 runs, using multithreading through processPooling (max_workers = nthreads)
    elapsed_time = benchmark.avg_count_clocks(progress_bar = progress_bar, f=pi.compute_pi_process_pool, n_runs=n_runs, n_threads=nthreads, max_workers = maxworkers, max_iterations = n_iterations)
    print(f"avg of {n_runs} (multithreading processPooling {nthreads} threads): {elapsed_time}")

    """
    print("pi no multithread   : ",pi.compute_pi(max_iterations = n_iterations))
    print("pi using multithread: ",pi.compute_pi_thread_pool(n_threads = nthreads, max_workers = maxworkers, max_iterations = n_iterations))
    print("pi split in two     : ", pi.compute_pi(start =0, max_iterations = int(n_iterations/2)) + pi.compute_pi(start = int(n_iterations/2), max_iterations = n_iterations))
    print("pi in math.pi       : ", math.pi)
    """
if(runmatrix == True):
    progress_bar = True
    elapsed_time = "N/A"

    # MATRIX MULTIPLICATION
    n = 100
    min_val = -10
    max_val = 10

    # getting the elapsed time of 1 run
if(testing == True):

    n = 10
    min_val = -10
    max_val = 10

    m = [ [1,2,3],[4,5,6],[7,8,9] ]

    print(matrix.matrix_mult(m1 = m, m2 = m))
