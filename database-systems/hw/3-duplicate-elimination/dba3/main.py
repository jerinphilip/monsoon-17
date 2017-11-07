from dba3.dtype import SimpleHashTable, HashTable
from dba3.dtype import Iterator
from dba3.dtype import BTree
from argparse import ArgumentParser

def opts(parser):
    parser.add_argument('-ds', '--container', choices=['btree', 'hashmap'], required=True, help="Container to use to find unique elements")
    parser.add_argument('-c', '--count', required=True, type=int, default=1000, help="Iterator load per iteration")
    parser.add_argument('-i', '--input', required=True, help="Input Record File")
    parser.add_argument('-o', '--output', required=True, help="File to write unique entries to")

if __name__ == '__main__':
    parser = ArgumentParser(description="Index structure, duplicate elimination")
    opts(parser)
    args = parser.parse_args()
    IS = SimpleHashTable()
    records = Iterator(input_file=args.input, max=args.count)
    if args.container == 'btree':
        IS = BTree(n=300, storage='data/btree', max_size=100000)
    else:
        IS = HashTable(buckets=10**6, max_size=10000, 
            storage='data/buckets')
    count = 0
    unique = 0
    with open(args.output, "w+") as uniq_f:
        for record in records:
            count = count + 1
            if record not in IS:
                unique += 1
                IS.add(record)
                print(','.join(map(str, record)), file=uniq_f)
            if count%1000 == 0:
                print("Unique: %d/%d"%(unique, count))


        print("Unique: %d/%d"%(unique, count))

