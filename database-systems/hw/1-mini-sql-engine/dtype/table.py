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

    def get(self, keys, fn, fname="tmp"):
        dataTranspose = []
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
        return self.data == self.data

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


    def _filter(self, attr, value, fn):
        if type(value) == list:
            index = self.indices[attr]
            data = []
            _, value = value
            for i, h in enumerate(self.dataTranspose[index]):
                #print(i, h)
                if fn(h, value): data.append(self.data[i])

            return Table(self.schema, data)
        else:
            print(attr, value)
            xi = self.indices[attr]
            yi = self.indices[value]
            data = []
            ps = zip(self.dataTranspose[xi], self.dataTranspose[yi])
            for i, p in enumerate(ps):
                x, y = p
                if fn(x, y): data.append(self.data[i])
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
