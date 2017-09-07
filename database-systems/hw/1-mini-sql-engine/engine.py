import sys, re, csv
import parser
from dtype import Table
from dtype import ops 
from pprint import pprint, pformat
from sqlparser import parse
from collections import OrderedDict
from store import Store, InvalidTable

class Engine:
    def __init__(self, storage):
        meta_file = "%s/metadata.txt"%(storage)
        self.metadata = {}
        self.metadata["tables"] = parser.meta(meta_file)
        self.store = Store(storage)
        for meta in self.metadata["tables"]:
            self.store.load(meta)

    def execute(self, query):
        asts = parse(query).asList()
        rs = []
        for ast in asts:
            env = OrderedDict()
            r = self.evaluate(ast, env)
            rs.append(r)
        return rs


    def evaluate(self, ast, env):
        key, value = ast

        error = lambda: "InternalError: \n%s"%(pformat(ast, indent=4))
        cases = {
            "Select": (lambda : self._select(value, OrderedDict())),
            "From": (lambda : self._from(value, env)),
            "Table": (lambda : self._table(value, env)),
            "Projection": (lambda : self._project(value, env)),
            "Where": (lambda : self._where(ast, env))
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
            "MAX": lambda : T.max(keys),
            "MIN": lambda : T.min(keys),
            "SUM": lambda : T.sum(keys),
            "AVG": lambda : T.avg(keys),
            "DISTINCT": lambda : T.distinct(keys),
            "ABS": lambda : T.abs(keys),
            "COUNT": lambda : T.count(keys)
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
                T = ops.tzip(T, self._feval(f, env))
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
            T = ops.product(T, S)
        env["result"] = T

        if env["where"] is not None:
            T = self.evaluate(env["where"], env)
            env["result"] = T
        return self.evaluate(env["project"], env)

    def _where(self, ast, env):
        where, tree = ast
        return self._bopEval(tree, env)

    def _bopEval(self, ast, env):
        """ From env[result], check elements which match ast. """
        op, args = ast
        tag, op = op
        x, y = args
        error = lambda: "Invalid Tree:%s"%(pformat(args))
        T = env["result"]
        cases = {
            "AND" : lambda : self._bopEval(x, env) & self._bopEval(y, env),
            "OR"  : lambda : self._bopEval(x, env) | self._bopEval(y, env),
            "="   : lambda : T.eq(x, y) ,
            "!="  : lambda : T.ne(x, y),
            "<"   : lambda : T.lt(x, y),
            ">"   : lambda : T.gt(x, y),
            ">="  : lambda : T.ge(x, y),
            "<="  : lambda : T.le(x, y),
        }

        return cases.get(op, error)()

if __name__ == '__main__':
    #name, command = sys.argv
    cursor = Engine("files")
    commands = open("sample.txt").read().splitlines()
    for lineno, command in enumerate(commands):
        print("\n"+"-"*10)
        print(lineno)
        print(command)
        try:
            results = cursor.execute(command)
            for table in results:
                print(table)
        except InvalidTable as e:
            print(e)

