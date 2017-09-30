from .base import IndexBase

class SimpleHashTable(IndexBase):
    def __init__(self):
        self.table = set()

    def __contains__(self, record):
        return record in self.table

    def add(self, record):
        self.table.add(record)

class Block:
    def __init__(self):
        self.fnames = []

    def add(self):
        pass


class HashTable(IndexBase):
    pass
