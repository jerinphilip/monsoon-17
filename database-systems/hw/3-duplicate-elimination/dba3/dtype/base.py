
class IndexBase:
    """ Abstract base class for an index structure """
    def __init__(self):
        pass

    def __contains__(self, x):
        raise NotImplementedError

    def add(self, x):
        raise NotImplementedError
