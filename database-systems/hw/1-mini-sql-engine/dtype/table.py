import operator as op
import dtype.dops as dops

class Table:
    def __init__(self, schema, data, original=True):
        self.schema = schema
        self.data = data
        self.dataTranspose = list(zip(*data))
        self.nrows = len(self.data)
        self.ncols = len(self.dataTranspose)
        attrs = schema["attributes"]
        self.indices = dict(zip(attrs, range(len(attrs))))
        table_names, cols = list(zip(*map(lambda x: x.split('.'), attrs)))
        self.ambiguous = dict(zip(cols, range(len(cols))))
        self.tables = list(set(table_names))
        self.inverse = dict([(col, []) for col in cols])
        for tn, col in zip(table_names, cols):
            self.inverse[col].append(tn)

    def __str__(self):
        pcol = lambda x: "%s"%(x)
        headers = list(map(pcol, self.schema["attributes"]))
        csv = lambda ls: ','.join(map(str, ls))
        header_string = csv(headers)
        data_strs = list(map(csv, self.data))
        meta_info = "%d rows, %d columns"%(self.nrows, self.ncols)
        out = '\n'.join([header_string , "-"*len(header_string)] + data_strs + ["-"*6, meta_info])
        return out

    def __getitem__(self, keys):
        return self.get(keys, lambda x: x, "id")

    def _namespaced_ls(self, keys):
        nkeys = []
        for key in keys:
            nkeys.append(self._namespaced(key))
        return nkeys

    def _namespaced(self, key):
        ls = key.split('.')
        if len(ls) == 1:
            ckey = ls[0]
            table = self.inverse[ckey][0]
            return "%s.%s"%(table, key)
        else:
            return key


    def get(self, keys, fn, fname="tmp"):
        dataTranspose = []
        types, keys = list(zip(*keys))
        keys = self._namespaced_ls(keys)
        schema = {"name": "%s(tmp)"%(fname), "attributes": keys}
        for key in keys:
            reduced = fn(self.dataTranspose[self.indices[key]])
            dataTranspose.append(reduced)
        data = list(zip(*dataTranspose))
        return Table(schema, data)


    def max(self, key):
        return self.get(key, dops.max_, "MAX")

    def min(self, key):
        return self.get(key, dops.min_, "MIN")

    def sum(self, key):
        return self.get(key, dops.sum_, "SUM")

    def avg(self, key):
        return self.get(key, dops.avg_, "AVG")

    def distinct(self, key):
        return self.get(key, dops.unique_, "DISTINCT")

    def abs(self, key):
        return self.get(key, dops.abs_, "ABS")

    def _bop(self, other, fn):
        assert(self.ncols == 1 and other.ncols == 1)
        assert(self.nrows == other.nrows)
        sfirst, *rest = self.dataTranspose
        ofirst, *rest = other.dataTranspose
        result = list(map(fn, sfirst, ofirst))
        schema = {
                "name": "R",
                "attributes": ["R"]
        }

        data = list(zip(*dataTranspose))
        return Table(schema, data)

    def __eq__(self, other):
        return self.data == other.data

    def __add__(self, other):
        return self._bop(self, other, op.add)
    
    def __mul__(self, other):
        return self._bop(self, other, op.mul)

    def __div__(self, other):
        return self._bop(self, other, op.div)

    def toTuple(self):
        x = tuple(map(tuple, self.data))
        return x

    def __and__(self, other):
        data = list(set(self.toTuple()) & set(other.toTuple()))
        return Table(self.schema, data)

    def __or__(self, other):
        data = list(set(self.toTuple()) | set(other.toTuple()))
        return Table(self.schema, data)


    def _filter(self, left, right, fn):
        ltype, lval = left
        rtype, rval = right
        lval = self._namespaced(lval)
        rval = self._namespaced(rval)
        if ltype == "Column" and rtype == "Column":
            xi = self.indices[lval]
            yi = self.indices[rval]
            data = []
            ps = zip(self.dataTranspose[xi], self.dataTranspose[yi])
            for i, p in enumerate(ps):
                x, y = p
                if fn(x, y): data.append(self.data[i])
            return Table(self.schema, data)
        else:
            index = self.indices[lval]
            data = []
            for i, h in enumerate(self.dataTranspose[index]):
                #print(i, h)
                if fn(h, rval): data.append(self.data[i])

            return Table(self.schema, data)

    def eq(self, attr, value):
        return self._filter(attr, value, op.eq)

    def lt(self, attr, value):
        return self._filter(attr, value, op.lt)

    def gt(self, attr, value):
        return self._filter(attr, value, op.gt)

    def ne(self, attr, value):
        return self._filter(attr, value, op.ne)

    def ge(self, attr, value):
        return self._filter(attr, value, op.ge)

    def le(self, attr, value):
        return self._filter(attr, value, op.le)
