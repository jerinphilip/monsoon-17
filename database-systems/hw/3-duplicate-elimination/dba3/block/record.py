from .block import Block

class RecordBlock:
    def __init__(self, **kwargs):
        self.block = Block(**kwargs)
        self.count = 0

    def tocsv(self, record):
        return ','.join(map(str, record))

    def fromcsv(self, line):
        if not line:
            return ()
        sts = line.split(',')
        return tuple(map(int, sts))

    def write(self, record):
        out = self.tocsv(record)
        self.block.write(out + '\n')

    def overwrite(self):
        self.block.overwrite()

    def read(self):
        content = self.block.read()
        lines = content.splitlines()
        data = []
        for line in lines:
            data.append(self.fromcsv(line))
        return data




