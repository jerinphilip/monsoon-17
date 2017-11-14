from collections import defaultdict
import random
from utils import epsgreedy

def SARSA(**kwargs):
    _sarsa = lambda t: t
    defaults = {
        "gamma": 0.99,
        "eps": 0.05
    }

    N = defaultdict(int)
    Q = defaultdict(random.random)
    defaults.update(kwargs)

    def policy():
        ls = list(range(4))
        states = product(ls, ls)
        pi = dict()
        for s in states:
            q_value = lambda a: Q[(s, a)]
            a = max(actions, key=q_value)
            pi[s] = a
        return pi

    def update(s, a, r, s_, a_):
        # _a = defaults["alpha"]
        _g = defaults["gamma"]
        N[(s, a)] += 1
        _a = 1/N[(s, a)]
        Q[(s, a)] = Q[(s, a)] + _a*(r + _g*Q[(s_, a_)] - Q[(s, a)])

    def choose(s_):
        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        q_value = lambda a: Q[(s_, a)]
        best_action = max(actions, key=q_value)
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

