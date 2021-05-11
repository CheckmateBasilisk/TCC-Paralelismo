print(">importing benchmark.py")

import time
# import threading
import concurrent.futures

from tqdm import tqdm

"""
these higher-order-funcions provide wrappers to compare performance
The wrappers ONLY ACCEPT NAMED ARGS
"""


# given funcion f (their keyword arguments kwargs, their positional arguments args)
# returns the nr of clocks needed to compute f
# WILL NOT TREAT MISUSE
# what a disgusting way to pass args... this is the only way it works in python... read comments[1] at the end
def count_clocks(*args, f=None, **kwargs):
    clock = time.time() # get current time
    f(*args,**kwargs) # compute f
    return time.time() - clock # get elapsed time


# TODO: adicionar intervalo de confiança e desvio padrão
# TODO: devo perturbar o cache entre execuções??? Faz sentido fazer isso??? Pq as vantagens do cache não podem ser parte da vantagem da linguagem 
# given function f (their positional arguments args, their keyword arguments kwargs)
# and number of runs n_runs
# returns the average nr of clocks needed to compute f
# WILL NOT TREAT MISUSE
def avg_count_clocks(*args, f=None, n_runs=1, **kwargs):
    avg_clock = 0
    # n jobs. doing each one after the last
    for i in tqdm(range(n_runs)): #tqdm is just a progress bar
        #print(f"running... {i+1}/{n}")
        avg_clock += count_clocks(f=f, *args,**kwargs) # if f has no positional args, this will work :)
    return avg_clock/n_runs


#TODO: tem algo errado na minha lógica. O programa com threads tá levando mto mais q o normal...
# threading tem que acontecer dentro da função de computação de pi, não na fç que faz a média!!!!!
# daqui pra baixo não tem nada de errado com o código em si, mas não faz sentido se preocupar em multiprocessar o cálculo das médias.

# given thread-safe function f (their positional arguments args, their keyword arguments kwargs)
# the number of runs n_runs
# and the number of threads n_threads
# returns the average nr of clocks needed to compute f
# using thread pooling to run n times on n_threads (ONLY AVAILABLE IN V3.2+)
# WILL NOT TREAT MISUSE
def avg_count_clocks_thread_pool(*args, f=None, n_runs=1, n_threads = 1, **kwargs):
    avg_clock = 0
    # starts threads, stores them in the thread array
    # submits n jobs for the n_threads workers to compute
    with concurrent.futures.ThreadPoolExecutor(max_workers = n_threads) as executor: # TODO: max_workers really defines the max amount of threads?
        # each execution of f is a job. Dividing jobs between threads:
        jobs = [ executor.submit(count_clocks,f=f, *args, **kwargs) for i in range(n) ]
        # joining (sync) threads
        for i,j in enumerate(tqdm(jobs)): #tqdm is just a progress bar
            #print(f"joining job (with {n_threads} workers) {i}/{n}")

            avg_clock += j.result()/n # if f has no positional args, this will work :)

    return avg_clock


"""
links usados
Python Threading Tutorial: Run Code Concurrently Using the Threading Module
    https://www.youtube.com/watch?v=IEEhzQoKtQU
"""


"""[1]
# example function with two named parameters
# might a good idea to use static typing to avoid having the wrapper screw things up
def printMe(string1="", string2=""):
    print(string1,string2)
    return

# wrapper that recieves f, anon parameters (args) and named parameters (kwargs)
# WILL NOT TREAT MISUSE!
def wrapper(a,b,c,*args, f=None, **kwargs):
    # kwargs is a dict.
    #print("kwargs is a {}", type(kwargs))
    # **kwargs unpacks it (dereferencing?)
    print(a,b,c)
    f(*args,**kwargs)

# since positional arguments need to come first, then keywords, the order of args gets a little weird
# this was my first attept and it didnt work because 1,2,3 were positional args after f, which is a keyword
# the only way to fix this and keep the order was to make args a keyworded tuple and unpack it inside the wrapper (using *), which is sooo lame
# wrapper(f=printMe, 1,2,3 , string1="Hello, There", string2="General Kenobi!") <- won't work
# wrapper(f=printMe, args=(1,2,3) , string1="Hello, There", string2="General Kenobi!")
# the only fix was to put the wrapper's positional args at the beginning, then the *args, **kwargs, and then the wrapper's keywords
# wrapper(<positional arguments>, *args, **kwargs, <keyword arguments>) <- like this
# luckily wrapper has no positiona arguments, which makes it less... ugly.

# wrapper(1,2,3, 4,5,6, f=printMe, string1 = "Hello There", string2 = "General Kenobi!") <- this works :p
# 1,2,3 are positional arguments of wrapper()
# 4,5,6 are positional arguments of printMe()
# f is positional argument of wrapper()
# string1, string2 are positional arguments of printMe()

# reading: https://towardsdatascience.com/10-examples-to-master-args-and-kwargs-in-python-6f1e8cc30749
"""
