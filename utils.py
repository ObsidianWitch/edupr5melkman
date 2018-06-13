import types

# Iterable SimpleNamespace.
class Table(types.SimpleNamespace):
    def __iter__(self):
        for k, v in self.__dict__.items(): yield v

class Iter:
    def __init__(self, collection):
        self.collection = collection
        self.i = -1

    @property
    def current(self):
        if self.collection:
            if self.i == -1: return self.collection[0]
            else:            return self.collection[self.i]

    @property
    def finished(self): return (self.i == len(self.collection) - 1)

    def next(self):
        if self.i + 1 < len(self.collection):
            self.i += 1
            return self.collection[self.i]

    def prev(self):
        if self.i - 1 >= 0:
            self.i -= 1
            return self.collection[self.i]
