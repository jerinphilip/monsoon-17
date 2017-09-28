from .base import IndexBase

class BTree(IndexBase):
    def __init__(self):
        pass

    def add(self, record):
        pass

    def __contains__(self, record):
        pass

class BTreeNode:
    def __init__(self, **kwargs):
        self.n = kwargs['n']
        self.keys = []
        self.children = []
        self.parent = None

    def violates(self):
        nkeys = len(self.keys)
        c1 = nkeys <= self.n
        c2 = len(self.children) == nkeys

    def full(self):
        return len(self.keys) == self.n

    def adopt(self, parent):
        self.parent = parent

    def split(self):
        mid = int(self.n/2)
        left_half = self.keys[:mid]
        right_half = self.keys[mid+1:]

    def add(self, record):
        if self.full()



if __name__ == '__main__':
    pass

