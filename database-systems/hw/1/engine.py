import sys, re, csv
import parser
from dtype import Table, zip_join
from pprint import pprint, pformat
from sqlparser import parse
from collections import OrderedDict
from store import Store
import dops

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

    def _feval(self, ast, env):
        tag, body = ast
        fn, cols = body
        _, keys = cols

        T = env["result"]
        error = lambda : "Error in feval"

        cases = {
            "MAX": lambda : T.get(keys, dops.max_, fn),
            "MIN": lambda : T.get(keys, dops.min_, fn),
            "SUM": lambda : T.get(keys, dops.sum_, fn),
            "AVG": lambda : T.get(keys, dops.avg_, fn),
            "DISTINCT": lambda : T.get(keys, dops.unique_, fn),
            "ABS": lambda : T.get(keys, dops.abs_, fn),
        }

        return cases.get(fn, error)()


    def _project(self, ast, env):
        T = env["result"]
        tag, rest = ast[0]
        error = lambda: "Invalid"

        def _fevals(cols):
            f, *fs = cols
            T = self._feval(f, env)
            for f in fs:
                T = zip_join(T, self._feval(f, env))
            return T

        cases = {
            "Columns": lambda : T[rest],
            "Functions": lambda : _fevals(rest),
            "All": lambda : T
        }
        return cases.get(tag, error)()

        
    def _table(self, ast, env):
        return self.store.project(ast)

    def _from(self, ast, env):
        tag, tables = ast
        first, *ts = tables
        T = self.evaluate(first, env)
        for t in ts:
            S = self.evaluate(t, env)
            T = zip_join(T, S)
        env["result"] = T
        return self.evaluate(env["project"], env)

    def _where(self, ast, env):
        pass

if __name__ == '__main__':
    name, command = sys.argv
    cursor = Engine("files")
    result = cursor.execute(command)
    print(result)


