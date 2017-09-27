from .block import Block

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




