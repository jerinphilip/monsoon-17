import random
from math import exp

def epsgreedy(**kwargs):
    best = kwargs['best']
    others = kwargs['others']
    eps = kwargs['eps']
    if random.random() < eps:
        return random.choice(others)
    return best
    

def safe_exp(x):
    ans = None
    try:
        ans = exp(x)
    except OverflowError:
        ans = float('inf')
    return ans

