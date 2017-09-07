from dtype import Table
import parser
from pprint import pprint

class Store:
    def __init__(self, storage):
        self.storage = storage
        self.store = {}
        self.inverse = {}
        self.temp = {}

    def load(self, meta):
        name = meta["name"]
        fname = "%s/%s.csv"%(self.storage, name)
        values = parser.table(meta, fname)
        self.store[name] = Table(meta, values)
        self.inverse_load(meta)

    def buffer(self, table):
        name = table.schema["name"]
        self.table.store[name] = table

    def inverse_load(self, meta):
        for attr in meta["attributes"]:
            if attr not in self.inverse:
                self.inverse[attr] = []
            self.inverse[attr].append(meta["name"])

    def display(self):
        for table in self.store:
            print("-"*10)
            print(self.store[table])

        print("Inverse:")
        pprint(self.inverse)

    def project(self, name, cols=None):
        if cols is None:
            if name in self.store:
                return self.store[name]
            else:
                raise InvalidTable(name)
        return self.store[name][cols]


class InvalidTable(Exception):
    def __init__(self, table):
        self.invalid = table

    def __str__(self):
        return "Error:\n%s: This table does not exist"%(self.invalid)
