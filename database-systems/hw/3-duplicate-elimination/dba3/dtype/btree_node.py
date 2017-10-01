import os
from dba3.block import RecordBlock

class BTreeNode:
    def __init__(self, **kwargs):
        self.n = kwargs['n']
        self.keys = []
        self.children = []
        self.i = kwargs['i']
        self.storage = kwargs['storage']
        self.max_size = kwargs['max_size']
        self.fname = os.path.join(self.storage, "node_%d.bt"%(self.i))
        self.load()

    def load(self):
        block = RecordBlock(name=self.fname, size=self.max_size)
        data = block.read()
        if data:
            self.children, *self.keys = data
            self.children = list(self.children)

    def save(self):
        block = RecordBlock(name=self.fname, size=self.max_size)
        block.overwrite()
        block.write(self.children)
        for key in self.keys:
            block.write(key)

    def check_constraints(self):
        nkeys = len(self.keys)
        c1 = nkeys <= self.n
        c2 = len(self.children) == nkeys
        return c1 and c2

    def full(self):
        return len(self.keys) == self.n

    def position(self, record):
        """
        Insertion happens at position
        """
        i = 0 
        while i < len(self.keys) \
            and self.keys[i] < record :
            i += 1
        return i

    def child(self, key):
        """
        node -> children
        i -> (i, i+1)
        pos returns index of first element greater than record
        Insert to the left of pos => insert at child[i]
        """
        j = self.position(key)
        return self.children[j]

    def add(self, record):
        assert(not self.full())
        i = self.position(record)
        self.keys.insert(i, record)
        return i

    def leaf(self):
        return not self.children

    def split(self):
        assert(self.full())
        mid = int(self.n/2)
        left_keys = self.keys[:mid]
        right_keys = self.keys[mid+1:]

        left_children = []
        right_children = []
        if self.children:
            left_children = self.children[:mid+1]
            right_children = self.children[mid+1:]

        left = (left_keys, left_children)
        right = (right_keys, right_children)
        return (self.keys[mid], left, right)

    def set(self, pack):
        keys, children = pack
        self.keys = keys
        self.children = children

    def __contains__(self, record):
        return record in self.keys



if __name__ == '__main__':
    import random
    import sys
    random.seed(100)
    from pprint import pprint
    node = BTreeNode(n=3, storage='data/btree', i=0, max_size=1000)

    """
    xs = random.sample(range(1, 100), 50)
    for x in xs:
        y = (x, 23)
        node.keys.append(y)

    xs = random.sample(range(1, 100), 7)
    for x in xs:
        node.children.append(x)
    """

    print(node.keys, node.children)
    node.save()
