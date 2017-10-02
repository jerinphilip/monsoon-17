import numpy as np
import math
from .distributions import Bernoulli
from .mab import MABLearner

class EXP3MAB(MABLearner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eta = math.sqrt(2*math.log(self.narms)/(self.narms*self.T))
        self.weights = [1.0/self.narms for i in range(self.narms)]

        # Initializing adversary
        self.delta = 0.1

        self.adversary = [Bernoulli(p=0.5) for i in range(8)]
        a9 = Bernoulli(p=(0.5 - self.delta))
        self.adversary.append(a9)
        a10 = Bernoulli(p=(0.5 + self.delta))
        self.adversary.append(a10)

        self.loss_estimator = [0.0 for i in range(self.narms)]
        self.losses = []
        self.choices = []
        self.obtained = 0
        self.modified_best = 0

    def reward(self, i):
        # Check if the 10th adversary requires change
        if 2*self.t >= self.T:
            self.adversary[10-1] = Bernoulli(p=(0.5 - 2*self.delta))

        loss = [self.adversary[i](self.t) for i in range(self.narms)]
        self.losses.append(loss)
        return loss[i]

    def update(self, i, x):
        EPS = 1e-9
        estimate_delta = x/(self.weights[i]+ EPS)
        self.loss_estimator[i] += estimate_delta

        projection = lambda x: math.exp(-1*self.eta*x)
        exp_space = map(projection, self.loss_estimator)
        exp_space = list(exp_space)

        denom = sum(exp_space)
        for i in range(self.narms):
            self.weights[i] = projection(self.loss_estimator[i])/(denom+EPS)

    def pseudo_regret(self):
        t = self.t - 1
        i = self.choices[t]
        self.obtained += self.losses[t][i]

        i = np.argmin(self.losses[t])
        self.modified_best += self.losses[t][i]

        return self.obtained - self.modified_best
        

    def choose_arm(self):
        i = np.argmax(self.weights)
        self.choices.append(i)
        return i

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    for T in [10**3, 10**4, 10**5]:
        H = EXP3MAB(n=10, T=T)
        print("T=%d"%(T))
        xs, ys = [], []
        for h in H:
            xs.append(h.t)
            ys.append(h.pseudo_regret())
        plt.plot(xs, ys)
        plt.show()






