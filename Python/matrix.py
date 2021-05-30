print(">importing matrix.py")

import random

# TODO: usar matriz de inteiros? talvez seja uma boa pra aplicação ser o menos CPU-bound possível. Na hora de escolher o intervalo dos números aleatórios pegar um intervalo simétrico em volta do zero pra evitar estourar os inteiros na hora da multiplicação!
# TODO: será q eh conveniente usar arrays ao invés de listas? isso acelera acesso a memória, mas eh isso q eu quero checar...
# given n and min_val and max_Val
# returns a n x n matrix with random values values in [min_val, max_val]
def get_random_int_matrix(n = 100, min_val = 0, max_val = 1):

    m = [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(n)]

    return m

# given square matrices m1 and m2
# returns the result m1 x m2
# Will not handle misuse!
def matrix_mult(m1 = None, m2 = None):
    result = None
    n = len(m1) # matrix size

    result=[ [i for i in range(n)] for j in range(n) ]

    return result
