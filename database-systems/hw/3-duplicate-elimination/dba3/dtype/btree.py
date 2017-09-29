from .base import IndexBase
from collections import OrderedDict

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
        self.leaf = True

        if 'keys' in kwargs: self.keys = kwargs['keys']
        if 'children' in kwargs: self.keys = kwargs['children']

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
        left_children = self.children[:mid+1]
        right_children = self.children[mid+1:]

        left = BTreeNode(keys=left_half, children=left_children, n=self.n)
        right = BTreeNode(keys=left_half, children=right_children, n=self.n)

        midkey = self.keys[mid]
        self.keys = [midkey]
        self.children = [left, right]
        self.leaf = False

        # Try to coalesce
        # Try to merge.

    def add(self, record):
        if self.leaf:
            if self.full():
                self.split()
                self.add(record)
            else:
                self.keys.append(record)
        else:
            count = 0
            for key in self.keys:
                if record > key:
                    break
                count = count + 1
            self.children[count].add(record)

    def export(self):
        entries = [("keys", self.keys)]
        if not self.leaf:
            childrenExport = list(map(lambda x: x.export(), self.children))
            childrenData = ("children", childrenExport)
            entries.append(childrenData)
        return OrderedDict(entries)


if __name__ == '__main__':
    import random
    random.seed(100)
    from pprint import pprint
    root = BTreeNode(n=4)
    for i in range(40):
        x = random.randint(1, 100)
        root.add(x)

    pprint(root.export())

