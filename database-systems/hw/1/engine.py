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
        ast = parse(query).asList()[0]
        env = OrderedDict() 
        self.evaluate(ast, env)

    def evaluate(self, ast, env):
        cases = []

        print(ast, len(ast))
        key, value = ast
        print("Key:", key)
        if key == 'Select':
            new_env = OrderedDict()
            T = self._select(value, new_env)
            env["result"] = T

        if key == 'From':
            self._from(value, env)

        if key == 'Tables':
            if len(value) == 1:
                name = value[0]
                env["result"] = self.tables[name]
                env["result"] = self._project(env)

    def _select(self, ast, env):
        f, w, p = ast
        env["where"] = w
        env["project"] = p
        self.evaluate(f, env)

    def _project(self, env):
        

    def _from(self, ast, env):
        self.evaluate(ast, env)





if __name__ == '__main__':
    name, command = sys.argv
    db = DB("files")
    db.execute(command)


