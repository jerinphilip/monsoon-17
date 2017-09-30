from collections import deque

class Iterator:
    def __init__(self, **kwargs):
        self.file = open(kwargs['input_file'], 'r')
        self.max = kwargs['max']
        self.count = 0
        self.buffer = deque()
        self.flag = True

    def tocsv(self, record):
        return ','.join(map(str, record))

    def fromcsv(self, line):
        sts = line.split(',')
        return tuple(map(int, sts))

    def __iter__(self):
        return self

    def __next__(self):
        if not self.empty():
            return self.get()
        else:
            if self.flag:
                self.buffered_io()
                return self.__next__()
            else:
                raise StopIteration

    def full(self):
        return self.count == self.max

    def empty(self):
        return self.count == 0
    
    def put(self, record):
        assert(not self.full())
        self.buffer.append(record)
        self.count = self.count + 1

    def get(self):
        assert(not self.empty())
        self.count = self.count - 1
        return self.buffer.popleft()


    def buffered_io(self):
        for line in self.file:
            stripped = line.strip()
            record = self.fromcsv(stripped)
            self.put(record)
            if self.full(): 
                self.flag =  True
                return True
        self.flag = False
        return False



if __name__ == '__main__':
    import sys
    records = Iterator(input_file=sys.argv[1], max=int(sys.argv[2]))
    for x in records:
        pass
