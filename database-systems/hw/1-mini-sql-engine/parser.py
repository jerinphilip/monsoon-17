import re
import csv

def meta(meta_fn):
    metadata = open(meta_fn).read()
    pattern = re.compile("<begin_table>\n([\s\S]*?)\n<end_table>")
    matches = pattern.findall(metadata)

    def load(match):
        name, *attrs = match.split('\n')
        d = dict([("name", name), ("attributes", attrs)])
        return d

    tables = list(map(load, matches))
    return tables

def table(meta, table_fn):
    """ File is csv, all entries integers """
    table_file = open(table_fn)
    reader = csv.reader(table_file)
    values = list(map(lambda row: list(map(int, row)), reader))
    return values

    

