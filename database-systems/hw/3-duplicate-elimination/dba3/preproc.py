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
                print(record)
                count += 1
        return required


    params = {
        "min": 100,
        "max": 200,
        "columns": 3,
        "count" : 100
    }

    output = RecordBlock(name=kw['output_file'], size=kw['size'])
    overflow = False
    while not overflow:
        params['min'] += 100
        params['max'] += 100
        rows = sample(**params)
        try:
            for row in rows:
                output.write(row)
            duplicates = random.sample(rows, kw['duplicates'])
            for row in duplicates:
                output.write(row)
        except BlockOverflowError:
            overflow = True

        
if __name__ == '__main__':
    kb = 1024
    random.seed(100)
    samples = generate(output_file='records.csv', 
            size=kb**3,
            duplicates=26)

