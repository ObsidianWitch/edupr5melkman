import types

# Iterable SimpleNamespace.
class Table(types.SimpleNamespace):
    def __iter__(self):
        for k, v in self.__dict__.items(): yield v

# Iterable keeping track of the current element.
class Iter:
    def __init__(self, collection):
        self.collection = collection
        self.i = -1

    @property
    def j(self): return self.i if self.i > -1 else 0

    def processed(self, reverse = False):
        return self.collection[0 : self.j + 1] if not reverse \
          else self.collection[self.j :: -1]

    def remaining(self): return self.collection[self.j + 1 :]

    @property
    def current(self):
        if self.collection: return self.collection[self.j]

    @property
    def finished(self): return (self.i == len(self.collection) - 1)

    def next(self):
        if self.i + 1 < len(self.collection):
            self.i += 1
            return self.collection[self.i]
