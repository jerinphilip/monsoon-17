import sys, re, csv
import parser
from dtype import Table
from pprint import pprint
from ast import AST
from sqlparser import simpleSQL

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
        statements = parse(query)
        context = {}


    def resolve(self, parsed, context):
        t = AST(parsed)
        print(parsed.tokens)
        pass



if __name__ == '__main__':
    name, command = sys.argv
    db = DB("files")
    db.execute(command)


