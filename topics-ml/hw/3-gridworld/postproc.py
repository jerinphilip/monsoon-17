from argparse import ArgumentParser
import csv
from matplotlib import pyplot as plt

parser = ArgumentParser()
parser.add_argument('-f', '--file', required=True)
args = parser.parse_args()

with open(args.file) as fp:
    reader = csv.reader(fp)
    data = list(reader)
    eps, ts, rs, srs, mrs, steps = list(zip(*data))
    ts = list(map(int, ts))
    mrs = list(map(float, mrs))
    steps = list(map(int, steps))
    plt.plot(ts, mrs, label="mean rewards")
    plt.plot(ts, steps, label="steps")
    plt.legend()
    plt.show()


