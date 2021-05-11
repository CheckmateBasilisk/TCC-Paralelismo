import pi
import matrix
import benchmark



"""
# TODO: apagar dps
def f(x = 0):
    return 2*x

import concurrent.futures
n_threads = 10
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread = [ executor.submit(f, i) for i in range(n_threads) ]
    for i in range(n_threads):
        print(f"{i+1}/{n_threads} : returned {thread[i].result()}")
"""



# COMPUTING PI
n_iterations = 1_000_000

# getting the elapsed time of 1 run, using 10m iterations
elapsed_time = benchmark.count_clocks(f = pi.compute_pi, iterations = n_iterations)
print(f"1 run: {elapsed_time}")

# getting the elapsed time of 100 runs, no threading
nruns = 30
elapsed_time = benchmark.avg_count_clocks(f=pi.compute_pi, n_runs=nruns, iterations = n_iterations)
print(f"avg of {nruns}: {elapsed_time}")

"""
# getting the elapsed time of 100 runs, using multithreading
nthreads = 8
elapsed_time = benchmark.avg_count_clocks_thread_pool(f=pi.compute_pi, n=nruns, n_threads=nthreads, iterations = n_iterations)
print(f"avg of {nruns}: {elapsed_time}")
"""

# getting the elapsed time of 100 runs, using multiprocessing




# MATRIX MULTIPLICATION
