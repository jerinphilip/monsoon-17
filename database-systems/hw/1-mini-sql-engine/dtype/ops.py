from .table import Table

def product(S, T):
    data = []
    attr = S.schema["attributes"] + T.schema["attributes"];
    schema = {
        "name": "product(%s, %s)"%(S.schema["name"], T.schema["name"]),
        "attributes": attr
    }
    for srow in S.data:
        for trow in T.data:
            data.append(srow + trow)
    return Table(schema, data)


def join_by(S, T, key):
    pass

def tzip(S, T):
    """ Default Join =>  Zip together. """
    if S.nrows != T.nrows:
        raise EntryMisMatchError
    else:
        attrs = S.schema["attributes"] + T.schema["attributes"]
        data = list(zip(*(S.dataTranspose + T.dataTranspose)))
        name = "zip_join(%s, %s)"%(S.schema["name"], T.schema["name"])
        schema = {"name": name, "attributes": attrs}
        return Table(schema, data)

