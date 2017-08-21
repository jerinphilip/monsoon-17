

def avg(ls):
    x = sum(ls)/len(ls)
    return x

def wrapped(fn):
    return lambda ls: [fn(ls)]

sum_ = wrapped(sum)
max_ = wrapped(max)
min_ = wrapped(min)
avg_ = wrapped(avg)
count_ = wrapped(len)

def unique_(ls):
    return list(set(ls))

def map_(fn):
    return lambda ls: list(map(fn, ls))

abs_ = map_(abs)

