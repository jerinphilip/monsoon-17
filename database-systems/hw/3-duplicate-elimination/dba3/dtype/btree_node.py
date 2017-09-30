
class BTreeNode:
    def __init__(self, **kwargs):
        self.n = kwargs['n']
        self.keys = []
        self.children = []
        self.i = kwargs['i']

        if 'keys' in kwargs: self.keys = kwargs['keys']
        if 'children' in kwargs: self.keys = kwargs['children']

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

