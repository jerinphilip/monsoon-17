
class MABLearner:
    def __init__(self, **kwargs):
        self.narms = kwargs['n']
        self.x = []
        self.T = kwargs['T']
        self.t = 0
        self.xt = []
        self.total = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.t = self.t + 1
        if self.t > self.T:
            self.t = self.t - 1
            raise StopIteration()
        i = self.choose_arm()
        x = self.reward(i)
        self.update(i, x)
        return self

    def choose_arm(self):
        raise NotImplementedError

    def reward(self, i):
        raise NotImplementedError

    def update(self, i, x):
        raise NotImplementedError

