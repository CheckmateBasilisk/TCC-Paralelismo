print(">importing pi.py")

# given the number of iterations
# computes pi using 'iterations' terms of a series
# defaults to 10 million iterations, wields 6 digit-precise pi
def compute_pi(iterations = 10_000_000):
    result = 0
    # i starting in 0 to iterations-1
    for i in range(iterations):
        # pi = 1 - 1/3 + 1/5 - 1/7 + 1/9 ... (-1)^i * 1/(2i-1)
        result += (-1)**i * 1/(i*2+1)
    result *= 4

    return(result)
