import numpy as np

class Distribution:
    def __init__(self, **kwargs):
        raise NotImplementedError

    def mean(self):
        raise NotImplementedError

    def var(self):
        raise NotImplementedError

    def __call__(self, t):
        raise NotImplementedError


class Bernoulli(Distribution):
    def __init__(self, **kwargs):
        self.p = kwargs['p']
        
    def mean(self):
        return self.p

    def var(self):
        return self.p*(1-self.p)

    def __call__(self, t):
        return np.random.binomial(1, self.p)



