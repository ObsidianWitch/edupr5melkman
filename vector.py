class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v): return self.__class__(
        self.x + v.x,
        self.y + v.y,
    )

    def __neg__(self): return self.__class__(
        -self.x,
        -self.y,
    )

    def __sub__(self, v): return self.__class__(
        self.x - v.x,
        self.y - v.y,
    )

    @classmethod
    def dot(self, va, vb): return (va.x * vb.x) + (va.y * vb.y)

    @classmethod
    def cross(self, va, vb): return (va.x * vb.y) - (va.y * vb.x)

    def __repr__(self): return f"<V2({self.x}, {self.y})>"
