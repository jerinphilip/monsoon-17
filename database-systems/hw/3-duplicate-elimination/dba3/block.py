
"""
Defines a block API.
* File wrapped around a class with constraints on datasize, for proof of
concept.  
* Change underlying code with same methods, get OS blocks.

"""

class BlockOverFlowError(Exception):
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
            raise BlockOverFlowError

        self.fp.write(output)
        self.size += len(output)

    def read(self):
        # Assuming a block, character IO
        contents = self.fp.read()
        self.size = len(contents)
        return contents


    def close(self):
        self.fp.close()

class RecordBlock(Block):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tocsv(self, record):
        return ','.join(map(str, record))

    def fromcsv(self, line):
        sts = line.split(',')
        return tuple(map(int, sts))

    def write(self, record):
        out = self.tocsv(record)
        super().write(out + '\n')

    def read(self):
        contents = super().read().splitlines()
        data = []
        for line in contents:
            data.append(self.fromcsv(line))
        return data

if __name__ == '__main__':
    block = Block(name='temp.txt', size=100)
    for i in range(102):
        block.write("1")




