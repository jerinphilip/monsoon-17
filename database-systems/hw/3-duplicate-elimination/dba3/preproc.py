import random
from dba3.block import RecordBlock, BlockOverflowError

def generate(**kw):
    """ Generates and write outs to a file """
    def sample(**kw):
        """
        Create a set of `count` distinct tuples 
            * entries within [min, max]
            * tuple columns  = columns
        """
        randentry = lambda x: random.randint(kw['min'], kw['max'])
        required = set()
        count = 0
        while count < kw['count']:
            record = tuple(map(randentry, range(kw['columns'])))
            if record not in required:
                required.add(record)
                count += 1
        return required


    params = {
        "min": 0,
        "max": 1000,
        "columns": 3,
        "count" : 100
    }

    output = open(kw['output_file'], "w+", 1024*1024*10)
    size = 0
    tocsv = lambda ls: ','.join(map(str, ls))
    while size < kw['size']:
        rows = sample(**params)
        for row in rows:
            crow = tocsv(row)
            size += len(crow)
            output.write(crow + '\n')
        duplicates = random.sample(rows, kw['duplicates'])
        for row in duplicates:
            crow = tocsv(row)
            size += len(crow)
            output.write(crow + '\n')
            


        
if __name__ == '__main__':
    kb = 1024
    random.seed(100)
    samples = generate(output_file='records.csv', 
            size=kb**2,
            duplicates=26)

