from .base import IndexBase
from dba3.block import RecordBlock, BlockOverflowError
import os

class SimpleHashTable(IndexBase):
    def __init__(self):
        self.table = set()

    def __contains__(self, record):
        return record in self.table

    def add(self, record):
        self.table.add(record)

class Bucket:
    def __init__(self, **kwargs):
        self.storage = kwargs['storage']
        self.hash = kwargs['hash']
        self.files = []
        self.count = 0
        self.max_size = kwargs['max_size']
        self.new()

    def add(self, record):
        try:
            block = RecordBlock(name=self.active, size=self.max_size)
            block.write(record)
            block.close()
        except BlockOverflowError:
            self.new()
            self.add(record)

    def __contains__(self, record):
        for fn in self.files:
            block = RecordBlock(name=fn, size=self.max_size)
            data = block.read()
            block.close()
            if record in data:
                return True
        return False
    
    def new(self):
        fname = "%s_%d.bkt"%(self.hash, self.count)
        fpath = os.path.join(self.storage, fname)
        self.active = fpath
        self.count += 1
        self.files.append(fpath)


class HashTable(IndexBase):
    def __init__(self, **kwargs):
        self.max_size = kwargs['max_size']
        self.buckets = kwargs['buckets']
        self.storage = kwargs['storage']
        self.count = 0
        self.hmap = {}

    def hash(self, record):
        return (sum(record))%(self.buckets)

    def add(self, record):
        value = self.hash(record)
        if value not in self.hmap:
            self.hmap[value] = Bucket(max_size=self.max_size, 
                    hash=value, storage=self.storage)
        self.hmap[value].add(record)
        self.count += 1

    def __len__(self):
        return self.count


    def __contains__(self, record):
        value = self.hash(record)
        if value not in self.hmap:
            return False
        return record in self.hmap[value]

if __name__ == '__main__':
    pass
