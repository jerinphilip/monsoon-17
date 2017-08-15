import sys, re, csv
import parser
from dtype import Table
from pprint import pprint
from sqlparser import parse
from collections import OrderedDict

class DB:
    def __init__(self, storage):
        meta_file = "%s/metadata.txt"%(storage)
        self.metadata = {}
        self.metadata["tables"] = parser.meta(meta_file)
        self.tables = {}
        for meta in self.metadata["tables"]:
            name = meta["name"]
            fname = "%s/%s.csv"%(storage, name)
            values = parser.table(meta, fname)
            self.tables[name] = Table(meta, values)

    def execute(self, query):
        ast = parse(query)
        env = OrderedDict()
        self.evaluate(ast, env)

    def evaluate(self, ast, env):
        #print("Final Dump:", ast.dump())
        #print("AsList:")
        pprint(ast.asList())
        pass





if __name__ == '__main__':
    name, command = sys.argv
    db = DB("files")
    db.execute(command)


