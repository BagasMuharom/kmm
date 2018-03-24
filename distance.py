import math

def euclidean(a, b):
    sigma = 0
    
    for i in range(len(a)):
        sigma += (a[i] - b[i]) ** 2
        
    return math.sqrt(sigma)

def manhattan(a, b):
    sigma = 0

    for i in range(len(a)):
        sigma += abs(a[i] - b[i])

    return sigma

def minkowsky(a, b, p = 2):
    sigma = 0

    for i in range(len(a)):
        sigma += (abs(a[i] - b[i]) ** p)
        
    return (sigma ** (1/p))