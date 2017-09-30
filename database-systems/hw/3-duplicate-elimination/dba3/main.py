from dba3.dtype import SimpleHashTable, HashTable
from dba3.dtype import Iterator
from dba3.dtype import BTree

if __name__ == '__main__':
    import sys
    IS = SimpleHashTable()
    IS = BTree(n=5)
    IS = HashTable(buckets=2000, max_size=10000000, 
            storage='data/buckets')
    records = Iterator(input_file=sys.argv[1], max=int(sys.argv[2]))
    for record in records:
        if record not in IS:
            IS.add(record)
    print(len(IS))
