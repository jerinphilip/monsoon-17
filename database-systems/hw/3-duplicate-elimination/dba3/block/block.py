
"""
Defines a block API.
* File wrapped around a class with constraints on datasize, for proof of
concept.  
* Change underlying code with same methods, get OS blocks.

"""

class BlockOverflowError(Exception):
    pass


class Block:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.max = kwargs['size']
        try:
            self.fp = open(self.name, 'x+')
            self.size = 0
        except FileExistsError:
            self.fp = open(self.name, 'r+')
            self.read()
            

    def write(self, output):
        if self.size + len(output) > self.max:
            raise BlockOverflowError

        self.fp.write(output)
        self.size += len(output)

    def read(self):
        # Assuming a block, character IO
        contents = self.fp.read()
        self.size = len(contents)
        return contents


    def close(self):
        self.fp.close()

if __name__ == '__main__':
    block = Block(name='temp.txt', size=100)
    for i in range(102):
        block.write("1")
