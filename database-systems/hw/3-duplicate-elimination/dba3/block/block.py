
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
        self.output = ''
        self.extra = ''
        if os.path.exists(self.name):
            self.fp = open(self.name, 'r+')
            self.output = self.fp.read()
        else:
            self.fp = open(self.name, 'w')

    def write(self, output):
        current = len(self.output) + len(self.extra)
        if current + len(output) > self.max:
            self.flush()
            raise BlockOverflowError
        self.extra += output

    def flush(self):
        lines = self.output.splitlines()
        self.fp.write(self.extra)

    def overwrite(self):
        self.fp = open(self.name, 'w+')

    def read(self):
        # Assuming a block, character IO
        return self.output

    def close(self):
        self.fp.close()

    def __del__(self):
        self.flush()
        self.close()

if __name__ == '__main__':
    block = Block(name='temp.txt', size=100)
    for i in range(102):
        block.write("1")
