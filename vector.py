class V2:
    def __init__(self, *args, index = None):
        self.index = index
        if len(args) == 1:
            self.x = args[0][0]
            self.y = args[0][1]
        else:
            self.x = args[0]
            self.y = args[1]

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
    def sign(cls, a): return 1 if a > 0 \
                      else -1 if a < 0 \
                      else 0

    # Given a left-handed 2D coordinate system:
    # Returns -1 if `c` (point) is on the left of `ab` (direction vector).
    # Returns  0 if `a`, `b` and `c` are collinear.
    # Returns  1 if `c` is on the right of `ab`.
    @classmethod
    def position(cls, a, b, c): return cls.sign(cls.cross(b - a, c - a))

    @classmethod
    def dot(cls, va, vb): return (va.x * vb.x) + (va.y * vb.y)

    @classmethod
    def cross(cls, va, vb): return (va.x * vb.y) - (va.y * vb.x)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self): return f"<V2({self.x}, {self.y})>"
