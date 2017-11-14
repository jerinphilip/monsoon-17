from collections import defaultdict
import random
from utils import epsgreedy, safe_exp
from itertools import product


def ExpectedSARSA(**kwargs):
    _sarsa = lambda t: t
    defaults = {
        "gamma": 0.99,
        "alpha": 0.01,
        "eps": 0.05,
        "a": 0.9,
        "b": 0.05,
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
        # _a = defaults["alpha"]
        _g = defaults["gamma"]
        N[(s, a)] += 1
        _a = 1/N[(s, a)]

        q_value = lambda a: Q[(s_, a)]
        best_action = max(actions, key=q_value)

        def pi(st, at):
            if at == best_action: return defaults["a"]
            negate = lambda x: -x
            if tuple(map(negate, at)) == a_: return 0
            return defaults["b"]

        EQ = sum([pi(s_, ta)*Q[(s_, ta)] for ta in actions])
        Q[(s, a)] = Q[(s, a)] + _a*(r + _g*EQ - Q[(s, a)])


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
    setattr(_sarsa, 'policy', policy)
    return _sarsa

if __name__ == '__main__':
    pass

