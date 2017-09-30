
"""
Defines a block API.
* File wrapped around a class with constraints on datasize, for proof of
concept.  
* Change underlying code with same methods, get OS blocks.

"""

import os

class BlockOverflowError(Exception):
    pass


class Block:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.max = kwargs['size']
        if os.path.exists(self.name):
            self.fp = open(self.name, 'r+')
            self.read()
        else:
            self.fp = open(self.name, 'w')
            self.size = 0

    def write(self, output):
        self.size += len(output)
        self.fp.write(output)

    def read(self):
        # Assuming a block, character IO
        self.fp = open(self.name, 'r+')
        data = self.fp.read()
        self.size = len(data)
        return data

    def close(self):
        self.fp.close()

if __name__ == '__main__':
    block = Block(name='temp.txt', size=100)
    for i in range(102):
        block.write("1")
