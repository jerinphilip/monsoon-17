from dba3.dtype import SimpleHashTable, HashTable
from dba3.dtype import Iterator
from dba3.dtype import BTree

if __name__ == '__main__':
    import sys
    IS = SimpleHashTable()

    count = int(sys.argv[2])
    IS = HashTable(buckets=2000, max_size=10000, 
            storage='data/buckets')
    IS = BTree(n=60, storage='data/btree', max_size=100000)
    records = Iterator(input_file=sys.argv[1], max=count)
    count = 0
    unique = 0
    for record in records:
        count = count + 1
        if record not in IS:
            unique += 1
            IS.add(record)
        if count % 1000 == 0:
            print("Unique: %d/%d"%(unique, count))

    print("Unique: %d/%d"%(unique, count))

