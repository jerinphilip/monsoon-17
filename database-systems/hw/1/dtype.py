class Table:
    def __init__(self, schema, data):
        self.schema = schema
        self.data = data
        self.dataTranspose = list(zip(*data))
        self.nrows = len(self.data)
        self.ncols = len(self.dataTranspose)
        attrs = schema["attributes"]
        self.indices = dict(zip(attrs, range(len(attrs))))

    def __str__(self):
        pcol = lambda x: "%s.%s"%(self.schema["name"], x)
        headers = list(map(pcol, self.schema["attributes"]))
        csv = lambda ls: ','.join(map(str, ls))
        header_string = csv(headers)
        data_strs = list(map(csv, self.data))
        meta_info = "%d rows, %d columns"%(self.nrows, self.ncols)
        out = '\n'.join([meta_info, header_string] + data_strs)
        return out

    def __getitem__(self, keys):
        dataTranspose = []
        schema = {"name": "tmp", "attributes": keys}
        for key in keys:
            dataTranspose.append(self.dataTranspose[self.indices[key]])
        data = list(zip(*dataTranspose))
        return Table(schema, data)

# Define binary operations on table.
# Any operator should return table.

def zip_join(S, T):
    """ Default Join =>  Zip together. """
    if S.nrows != T.nrows:
        raise EntryMisMatchError
    else:
        attrs = S.schema["attributes"] + T.schema["attributes"]
        data = list(zip(*(S.dataTranspose + T.dataTranspose)))
        name = "zip_join(%s, %s)"%(S.schema["name"], T.schema["name"])
        schema = {"name": name, "attributes": attrs}
        return Table(schema, data)

class EntryMisMatchError:
    pass
