from collections import defaultdict
import random
from utils import epsgreedy, safe_exp


def ExpectedSARSA(**kwargs):
    _sarsa = lambda t: t
    defaults = {
        "gamma": 0.99,
        "alpha": 0.01,
        "eps": 0.05
    }

    N = defaultdict(int)
    Q = defaultdict(random.random)
    defaults.update(kwargs)
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    pi = lambda s, a: safe_exp(Q[(s, a)])/sum([safe_exp(Q[(s, a)]) for a in actions])

    def update(*args):
        s, a, r, s_, a_ = args
        # _a = defaults["alpha"]
        _g = defaults["gamma"]
        N[(s, a)] += 1
        _a = 1/N[(s, a)]
        EQ = sum([pi(s, ta)*Q[(s, ta)] for ta in actions])
        Q[(s, a)] = Q[(s, a)] + _a*(r + _g*EQ - Q[(s, a)])
        print(s, s_)


    def choose(s_):
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
