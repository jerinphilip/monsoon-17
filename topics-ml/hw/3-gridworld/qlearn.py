from collections import defaultdict
import random
from utils import epsgreedy
from itertools import product

def QLearn(**kwargs):
    _sarsa = lambda t: t
    defaults = {
        "gamma": 0.99,
        "eps": 0.05
    }

    N = defaultdict(int)
    Q = defaultdict(random.random)
    defaults.update(kwargs)
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def policy():
        ls = list(range(4))
        states = product(ls, ls)
        pi = dict()
        for s in states:
            q_value = lambda a: Q[(s, a)]
            a = max(actions, key=q_value)
            pi[s] = a
        return pi


    def update(*args):
        s, a, r, s_, a_ = args
        _g = defaults["gamma"]
        #Q[(s, a)] = Q[(s, a)] + _a*(r + _g*Q[(s_, a_)] - Q[(s, a)])
        N[(s, a)] += 1
        _a = 1/N[(s, a)]

        q_value = lambda a: Q[(s_, a)]
        a_ = max(actions, key=q_value)
        Q[(s, a)] = (1-_a)*Q[(s, a)] + _a * (r + _g*Q[(s_, a_)])

    def choose(s_):
        q_value = lambda a: Q[(s_, a)]
        best_action = max(actions, key=q_value)
        # print(s_, "(best)", best_action)
        # TODO implement epsilon delta here.
        return epsgreedy(
                best=best_action,
                others=list(set(actions) - set([best_action])),
                eps=defaults["eps"])

    setattr(_sarsa, 'update', update)
    setattr(_sarsa, 'choose', choose)
    return _sarsa

if __name__ == '__main__':
    pass

