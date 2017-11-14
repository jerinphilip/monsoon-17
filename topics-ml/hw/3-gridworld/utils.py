import random

def epsgreedy(**kwargs):
    best = kwargs['best']
    others = kwargs['others']
    eps = kwargs['eps']
    if random.random() < eps:
        return random.choice(others)
    return best
    
