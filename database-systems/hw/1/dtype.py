class Table:
    def __init__(self, schema, data):
        self.schema = schema
        self.data = data
        self.dataTranspose = list(zip(*data))

    def __str__(self):
        pcol = lambda x: "%s.%s"%(self.schema["name"], x)
        headers = list(map(pcol, self.schema["attributes"]))
        csv = lambda ls: ','.join(map(str, ls))
        header_string = csv(headers)
        data_strs = list(map(csv, self.data))
        out = '\n'.join([header_string] + data_strs)
        return out

# Define binary operations on table.
# Any operator should return table.
