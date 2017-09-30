from dba3.dtype import SimpleHashTable
from dba3.dtype import Iterator
from dba3.dtype import BTree

if __name__ == '__main__':
    import sys
    IS = SimpleHashTable()
    IS = BTree(n=5)
    records = Iterator(input_file=sys.argv[1], max=int(sys.argv[2]))
    for record in records:
        if record not in IS:
            IS.add(record)
    print(len(IS))
