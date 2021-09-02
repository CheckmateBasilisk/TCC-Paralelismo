from math import floor, ceil
# import threading
import concurrent.futures

# when this is called by the manager, it should put into the stdout the elapsed time for computing pi
# it will recieve one parameter: the number of threads
# when nrThreads == 0, the non-threaded version should run
def main():
    import time
    import sys

    nthreads = int(sys.argv[1]) # paramaeter passed to script
    maxworkers = nthreads
    n_iterations = 1_000_000_000 # 1b iterations

    elapsed_time = time.time() # get current time
    if(nthreads == 0):
        compute_pi(max_iterations = n_iterations)
    elif(sys.argv[2] == "thread"):
        compute_pi_thread_pool(max_iterations = n_iterations, n_threads = nthreads, max_workers = maxworkers)
    elif(sys.argv[2] == "process"):
        compute_pi_process_pool(max_iterations = n_iterations, n_threads = nthreads, max_workers = maxworkers)
    elapsed_time = time.time() - elapsed_time # get elapsed time

    print(elapsed_time)
    return elapsed_time


# computing pi using Leibniz's Formula
# given the number of max_iterations
# computes pi using 'max_iterations' terms of a series (Leibniz's Formula)
# defaults to 10 million max_iterations, wields 6 digit-precise pi
# the series starts at a given term, defaults to 0. Anything other than 0 won't compute pi properly but is useful for splitting the workload
def compute_pi(start = 0, max_iterations = 10_000_000):
    result = 0
    # i starting in 0 to max_iterations-1
    for i in range(start, max_iterations):
        # pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 ... (-1)^i * 1/(2i-1)
        result += 4 * (-1)**i * 1/(i*2+1)

    return(result)



# given the number of max_iterations
# computes pi using 'max_iterations' terms of a series
# using thread pooling to compute pi n_threads with max_workers(ONLY AVAILABLE IN V3.2+)
# defaults to 10 million max_iterations, wields 6 digit-precise pi
# the series starts at a given term, defaults to 0. Anything other than 0 won't compute pi properly but is useful to split the workload
def compute_pi_thread_pool(max_iterations = 10_000_000, n_threads = 1, max_workers = 1):
    pi = 0
    # starts threads, stores them in the thread array
    # submits jobs (threads) for the workers to compute
    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor: # TODO: max_workers really defines the max amount of threads?
        # splitting the workload between threads
        # starts at i*max_iterations/n_threads goes to (i+1)*max_iterations/n_threads (range goes from 0 to nthreads-1)
        # each thread computes max_iterations/n_threads of the total workload
        # TODO: estou dividindo o trabalho errado. Algum termo do pi multithread está sendo computado mais vezes? ou será erro de arredondamento?
        #   to computando max_iterations+1 termos? NOPE
        #   floor/ceil? NOPE
        jobs = [
            executor.submit(compute_pi, start=int(i*max_iterations/n_threads), max_iterations=int((i+1)*max_iterations/n_threads))
            for i in range(n_threads) ]
        # joining (sync) threads
        for i,j in enumerate(jobs): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")
            pi += j.result() # if f has no positional args, this will work :)
    return pi


# given the number of max_iterations
# computes pi using 'max_iterations' terms of a series
# using process pooling to compute pi n_threads with max_workers(ONLY AVAILABLE IN V3.2+)
# defaults to 10 million max_iterations, wields 6 digit-precise pi
# the series starts at a given term, defaults to 0. Anything other than 0 won't compute pi properly but is useful to split the workload
def compute_pi_process_pool(max_iterations = 10_000_000, n_threads = 1, max_workers = 1):
    pi = 0
    # starts threads, stores them in the thread array
    # submits jobs (threads) for the workers to compute
    with concurrent.futures.ProcessPoolExecutor(max_workers = max_workers) as executor: # TODO: max_workers really defines the max amount of threads?
        # splitting the workload between threads
        # starts at i*max_iterations/n_threads goes to (i+1)*max_iterations/n_threads (range goes from 0 to nthreads-1)
        # each thread computes max_iterations/n_threads of the total workload
        # TODO: estou dividindo o trabalho errado. Algum termo do pi multithread está sendo computado mais vezes? ou será erro de arredondamento?
        #   to computando max_iterations+1 termos? NOPE
        #   floor/ceil? NOPE
        jobs = [
            executor.submit(compute_pi, start=int(i*max_iterations/n_threads), max_iterations=int((i+1)*max_iterations/n_threads))
            for i in range(n_threads) ]
        # joining (sync) threads
        for i,j in enumerate(jobs): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")
            pi += j.result() # if f has no positional args, this will work :)
    return pi





# computing pi using Wallis Product
# it seems to converge slower towards pi than the Leibniz Formula
def compute_pi_wallis(start = 0, max_iterations = 10_000_000):
    result = 1
    # i starting in 0 to max_iterations-1
    for i in range(start, max_iterations):
        # PI/2 = 2/1 * 2/3 * 4/3 * 4/5 * 6/5 * 6/7 * ... (ceil( (i+1)/2 )*2)/()
        result *= (ceil((i+1)/2)*2) / (ceil(i/2)*2 +1)
    result *= 2

    return(result)


if __name__ == "__main__":
    main()
