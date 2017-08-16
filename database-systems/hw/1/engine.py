import sys, re, csv
import parser
from dtype import Table, zip_join
from pprint import pprint, pformat
from sqlparser import parse
from collections import OrderedDict
from store import Store

class Engine:
    def __init__(self, storage):
        meta_file = "%s/metadata.txt"%(storage)
        self.metadata = {}
        self.metadata["tables"] = parser.meta(meta_file)
        self.store = Store(storage)
        for meta in self.metadata["tables"]:
            self.store.load(meta)

    def execute(self, query):
        ast = parse(query).asList()[0]
        env = OrderedDict()
        return self.evaluate(ast, env)

    def evaluate(self, ast, env):
        key, value = ast

        error = lambda: "InternalError: \n%s"%(pformat(ast, indent=4))
        cases = {
            "Select": (lambda : self._select(value, OrderedDict())),
            "From": (lambda : self._from(value, env)),
            "Table": (lambda : self._table(value, env)),
            "Projection": (lambda : self._project(value, env)),
        }
    
        v = cases.get(key, error)
        return v()


    def _select(self, ast, env):
        f, w, p = ast
        env["where"] = w
        env["project"] = p
        return self.evaluate(f, env)


    def _project(self, ast, env):
        T = env["result"]
        print(ast)
        return T

        
    def _table(self, ast, env):
        Id = ast[0]
        return self.store.project(Id)

    def _from(self, ast, env):
        tag, tables = ast
        first, *ts = tables
        T = self.evaluate(first, env)
        for t in ts:
            S = self.evaluate(t, env)
            T = zip_join(T, S)
        env["result"] = T
        return self.evaluate(env["project"], env)

if __name__ == '__main__':
    name, command = sys.argv
    cursor = Engine("files")
    result = cursor.execute(command)
    print(result)


