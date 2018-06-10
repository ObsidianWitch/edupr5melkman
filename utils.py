import types

# Iterable SimpleNamespace.
class Table(types.SimpleNamespace):
    def __iter__(self):
        for k, v in self.__dict__.items(): yield v
