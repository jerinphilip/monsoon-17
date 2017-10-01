from .base import IndexBase
from collections import OrderedDict, deque
from .btree_node import BTreeNode


class Directory:
    def __init__(self, **kwargs):
        self.storage = kwargs['storage']
        self.n = kwargs['n']
        self.max = kwargs['max_size']
        self.active = None

    def __getitem__(self, i):
        node = BTreeNode(n=self.n, i=i, storage=self.storage, max_size=self.max)
        return node
    


class BTree(IndexBase):
    def __init__(self, **kwargs):
        self.nodes = Directory(**kwargs)
        self.count = 0
        self.root = 0
        self.length = 0
        self.n = kwargs['n']
        # root = BTreeNode(n=self.n, i=0)
        # self.nodes.append(root)

    def add(self, record):
        self.length += 1
        root = self.nodes[self.root]
        if root.full():
            x = self.allocate()

            # Make new root
            y = self.root
            self.root = x

            nx = self.nodes[x]
            nx.children.append(y)
            nx.save()

            z = self.split(x, y)
            self.insert_non_full(x, record)
        else:
            self.insert_non_full(self.root, record)

    def split(self, x, y):
        z = self.allocate()

        ny = self.nodes[y]
        mid, left, right = ny.split()
        ny.set(left)
        ny.save()

        nz = self.nodes[z]
        nz.set(right)
        nz.save()

        nx = self.nodes[x]
        i = nx.add(mid)
        nx.children.insert(i+1, z)
        nx.save()
        return z


    def allocate(self):
        self.count += 1
        # right = BTreeNode(n=self.n, i=self.count)
        # self.nodes.append(right)
        return self.count
        

    def insert_non_full(self, i, key):
        ni = self.nodes[i]
        if ni.leaf():
            ni.add(key)
            ni.save()
        else:
            # Find child where key belongs
            # print("Path: ", self.nodes[i].keys)
            j = ni.child(key)
            nj = self.nodes[j]
            if nj.full():
                k = self.split(i, j)
                self.insert_non_full(i, key)
            else:
                self.insert_non_full(j, key)

    def export(self):
        return self._export(self.root)

    def _export(self, i):
        node = self.nodes[i]
        ls = [("keys", node.keys)]
        if not node.leaf():
            childExportData = []
            for child in node.children:
                childExportData.append(self._export(child))
            ls.append(("children", childExportData))
        return OrderedDict(ls)

    def _dot(self, x):
        entries = []
        # Nodes
        keys =  x.keys
        cells = []
        i = 0
        for key in keys:
            cell = "<c%d> | %s "%(i, key)
            i += 1
            cells.append(cell)

        label = "%s | <c%d>"%('|'.join(cells), i)
        node = "node_%d [label=\"%s\"];"%(x.i, label)
        entries.append(node)
        # Edges
        for i, c in enumerate(x.children):
            child = self.nodes[c]
            subtree = self._dot(child)
            entries.extend(subtree)
            entries.append("node_%s:c%d -> node_%s;"%(x.i, i, child.i))

        return entries

    def dot(self):
        params = [
            "node [shape=record];"
        ]
        entries = self._dot(self.nodes[self.root])
        body = '\n'.join(params + entries)
        return "digraph G {\n%s\n}"%(body)


    def __contains__(self, record):
        i = self.root
        node = self.nodes[i]
        while not node.leaf():
            if record in node:
                return True
            j = node.child(record)
            node = self.nodes[j]
        return record in node

    def __len__(self):
        return self.length


if __name__ == '__main__':
    import random
    import sys
    random.seed(100)
    from pprint import pprint
    tree = BTree(n=3, storage='data/btree', max_size=1000)
    xs = []

    ys = random.sample(range(1, 100), 50)
    for x in ys:
        xs.append(x)
        before = x in tree
        tree.add(x)
        after = x in tree
        print(x, "Before:", before, "| After:", after)
        if before == after:
            break
    print(tree.export())
    print(tree.dot(), file=open("rep.dot", "w+"))


