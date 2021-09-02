import random
# import threading
import concurrent.futures



def main():
    import time
    import sys

    nthreads = int(sys.argv[1]) # paramaeter passed to script
    maxworkers = nthreads
    n = 1000 #matrix size

    m1 = get_random_int_matrix(n = n, min_val = -10, max_val = 10,)
    m2 = get_random_int_matrix(n = n, min_val = -10, max_val = 10,)
    # matrix innitialization won't contribute to elapesed time
    result = [[0 for _ in range(n)] for _ in range(n)]

    elapsed_time = time.time() # get current time
    if(nthreads == 0):
        matrix_mult(m1=m1, m2=m2, result=result)
    elif(sys.argv[2] == "thread"):
        matrix_mult_thread_pool(m1=m1, m2=m2, n_threads = nthreads, max_workers = maxworkers, result=result)
    elif(sys.argv[2] == "process"):
        matrix_mult_process_pool(m1=m1, m2=m2, n_threads = nthreads, max_workers = maxworkers, result=result)
    elapsed_time = time.time() - elapsed_time # get elapsed time

    print(elapsed_time)
    return elapsed_time




# TODO: usar matriz de inteiros? talvez seja uma boa pra aplicação ser o menos CPU-bound possível. Na hora de escolher o intervalo dos números aleatórios pegar um intervalo simétrico em volta do zero pra evitar estourar os inteiros na hora da multiplicação!
# TODO: será q eh conveniente usar arrays ao invés de listas? isso acelera acesso a memória, mas eh isso q eu quero checar...
# given n and min_val and max_Val
# returns a n x n matrix with random int values values in [min_val, max_val]
# pseudorandom values obtained with given seed. if None, system time is used
def get_random_int_matrix(n = 100, min_val = 0, max_val = 1, seed=None):

    random.seed(seed)
    m = [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(n)]

    return m

# given square matrices m1 and m2
# and an alredy innitialized result matrix to store the result
# returns the result m1 x m2 (if rows==Null)
# Will not handle misuse!
# result should be innitialized outside so it doesn't contribute to the elapsed time
# in theory, innitializing the matrix should be inconsequential, since it is O(n^2) and the multiplication itself id O(n^3)
def matrix_mult(m1 = None, m2 = None, result = None):
    n = len(m1) # matrix size
    compute_rows(m1, m2, result, range(n))#computes all rows

    return result

# this is just a subroutine to compute a set of rows. Useful for threading
# computes rows in the slice rows=slice(start,end)
def compute_rows(m1, m2, result, rows):
    n = len(m1) # matrix size

    for i in rows:
        for j in range(n):
            # get item multiplying row of m1 and col of m2
            for k in range(n):
                result[i][j] += m1[k][j] * m2[i][k]

    return result #TODO is this needed??? it relies on collateral effects so it shouldnt need to return anything

"""
    for i in range(n):
        from functools import reduce
        # computes a single element of m1*m2
        reduce(lambda x,y: x+y, map(lambda x,y: x*y, l1,l2),0)
"""


# given square matrices m1 and m2
# and an alredy innitialized result matrix to store the result
# the number of threads and maximum nr of workers
# returns the result m1 x m2, computed using threadPools
# Will not handle misuse!
# result should be innitialized outside so it doesn't contribute to the elapsed time
# in theory, innitializing the matrix should be inconsequential, since it is O(n^2) and the multiplication itself id O(n^3)
def matrix_mult_thread_pool(m1 = None, m2 = None, result = None, n_threads = 1, max_workers = 1):
    n = len(m1) # matrix size

    # TODO: como eu vou quebrar a multiplicação de matriz??? ç__ç não queria ter que me dar o trabalho de criar uma fç só para computar uma linha da matriz
    # starts threads, stores them in the thread array
    # submits jobs (threads) for the workers to compute
    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor: # TODO: max_workers really defines the max amount of threads?
        jobs = [
            executor.submit(compute_rows, m1=m1, m2=m2, result=result, rows=range(int(i*n/n_threads),int((i+1)*n/n_threads)))
            for i in range(n_threads) ]
        # joining (sync) threads
        for i,j in enumerate(jobs): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")
            j.result() # if f has no positional args, this will work :)

    return result


# given square matrices m1 and m2
# and an alredy innitialized result matrix to store the result
# the number of threads and maximum nr of workers
# returns the result m1 x m2, computed using processPools
# Will not handle misuse!
# result should be innitialized outside so it doesn't contribute to the elapsed time
# in theory, innitializing the matrix should be inconsequential, since it is O(n^2) and the multiplication itself id O(n^3)
def matrix_mult_process_pool(m1 = None, m2 = None, result = None, n_threads = 1, max_workers = 1):
    n = len(m1) # matrix size

    # TODO: como eu vou quebrar a multiplicação de matriz??? ç__ç não queria ter que me dar o trabalho de criar uma fç só para computar uma linha da matriz
    # starts threads, stores them in the thread array
    # submits jobs (threads) for the workers to compute
    with concurrent.futures.ProcessPoolExecutor(max_workers = max_workers) as executor: # TODO: max_workers really defines the max amount of threads?
        jobs = [
            executor.submit(compute_rows, m1=m1, m2=m2, result=result, rows=range(int(i*n/n_threads),int((i+1)*n/n_threads)))
            for i in range(n_threads) ]
        # joining (sync) threads
        for i,j in enumerate(jobs): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")
            j.result() # if f has no positional args, this will work :)

    return result

if __name__ == "__main__":
    main()
