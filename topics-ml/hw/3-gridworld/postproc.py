from argparse import ArgumentParser
import csv
from matplotlib import pyplot as plt
from itertools import product
import pickle

def data(csvfile):
    with open(csvfile) as fp:
        reader = csv.reader(fp)
        data = list(reader)
        eps, ts, rs, srs, mrs, steps = list(zip(*data))
        ts = list(map(int, ts))
        mrs = list(map(float, mrs))
        steps = list(map(int, steps))
        return (ts, mrs, steps)

algos = [
            'qlearn', 
            'esarsa', 
            'sarsa'
        ]
eps = ['0.05', '0.2']

fname = lambda x: '-'.join(x)
fpath = lambda x: 'exps/' + fname(x) + '.csv'

files = list(product(algos, eps))
for pair in files:
    ts, mrs, steps = data(fpath(pair))
    plt.plot(ts, mrs, label="{}".format(fname(pair)))

plt.legend()
plt.show()

for pair in files:
    ts, mrs, steps = data(fpath(pair))
    plt.plot(ts, steps, label="{}".format(fname(pair)))

plt.legend()
plt.show()

symbol = {
    (0, 1): '>',
    (0, -1): '<',
    (1, 0): 'v',
    (-1, 0): '^'
}

for pair in files:
    pfpath = lambda x: 'exps/' + fname(x) + '.policy'
    vfpath = lambda x: 'exps/' + fname(x) + '.value'

    with open(pfpath(pair), "rb") as fp:
        pi = pickle.load(fp)
        print(fname(pair))
        for i in range(4):
            for j in range(4):
                s = (i, j)
                a = pi[s]
                print(symbol[a], end='')
            print()

    with open(vfpath(pair), "rb") as fp:
        V = pickle.load(fp)
        print(fname(pair))
        for i in range(4):
            for j in range(4):
                s = (i, j)
                print(V[s], end='\t')
            print()
