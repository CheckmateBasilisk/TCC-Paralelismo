import random
# import threading
import concurrent.futures

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
# optionally a slice rows=slice(start,end)
# returns the result m1 x m2 (if rows==Null)
# else, will compute only the rows in the slice
# Will not handle misuse!
def matrix_mult(m1 = None, m2 = None, rows=None):
    n = len(m1) # matrix size
    if(rows == None):
        rows = range(n)
    # is this performant enough? i think so. innitializing is insignificant when compared to the rest
    result = [[0 for _ in range(n)] for _ in range(n)]
    matrix_mult_idk(m1, m2, result, rows)

    return result


#TODO: find a decent name for this
def matrix_mult_idk(m1, m2, result, rows):
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

#TODO: INCOMPLETE
# TODO: tirar a inicialização da matriz!!!
# given square matrices m1 and m2
# returns the result m1 x m2
# Will not handle misuse!
def matrix_mult_thread_pool(m1 = None, m2 = None, n_threads = 1, max_workers = 1):
    n = len(m1) # matrix size
    # is this performant enough? i think so. innitializing is insignificant when compared to the rest
    result = [[0 for _ in range(n)] for _ in range(n)]

    pass

    # TODO: como eu vou quebrar a multiplicação de matriz??? ç__ç não queria ter que me dar o trabalho de criar uma fç só para computar uma linha da matriz
    # starts threads, stores them in the thread array
    # submits jobs (threads) for the workers to compute
    with concurrent.futures.ThreadPoolExecutor(max_workers = max_workers) as executor: # TODO: max_workers really defines the max amount of threads?
        jobs = [
            executor.submit(compute_pi, start=int(i*max_iterations/n_threads), max_iterations=int((i+1)*max_iterations/n_threads))
            for i in range(n_threads) ]
        # joining (sync) threads
        for i,j in enumerate(jobs): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")
            pi += j.result() # if f has no positional args, this will work :)
    return pi


    for i in range(n):
        for j in range(n):
            # get item multiplying row of m1 and col of m2
            for k in range(n):
                result[i][j] += m1[k][j] * m2[i][k]

    return result

#TODO: INCOMPLETE
# given square matrices m1 and m2
# returns the result m1 x m2
# Will not handle misuse!
def matrix_mult_process_pool(m1 = None, m2 = None, n_threads = 1, max_workers = 1):
    n = len(m1) # matrix size
    # is this performant enough? i think so. innitializing is insignificant when compared to the rest
    result = [[0 for _ in range(n)] for _ in range(n)]

    pass

    for i in range(n):
        for j in range(n):
            # get item multiplying row of m1 and col of m2
            for k in range(n):
                result[i][j] += m1[k][j] * m2[i][k]

    return result
