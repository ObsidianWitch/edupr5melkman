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

    def __eq__(self, v): return (self.x == v.x) and (self.y == v.y)

    @classmethod
    def sign(cls, a): return 1 if a > 0 \
                        else -1 if a < 0 \
                        else 0

    # Given a left-handed 2D coordinate system:
    # Returns -1 if `c` (point) is on the left of `ab` (direction vector) -> CCW.
    # Returns  0 if `a`, `b` and `c` are collinear.
    # Returns  1 if `c` is on the right of `ab` -> CW.
    @classmethod
    def rotation(cls, a, b, c): return cls.sign(cls.cross(b - a, c - a))

    # Returns -1 if `c` (point) if behind `ab` (direction vector).
    # Returns  0 if `c` is inside `ab`.
    # Returns  1 if `c` is in front of `ab`.
    def position(a, b, c):
        inside = (V2.sign(V2.dot(a - c, b - c)) <= 0)
        behind = (V2.sign(V2.dot(b - a, c - a)) < 0)
        front = (not behind) and (not inside)
        return  1 if front \
          else  0 if inside \
          else -1

    @classmethod
    def dot(cls, va, vb): return (va.x * vb.x) + (va.y * vb.y)

    @classmethod
    def cross(cls, va, vb): return (va.x * vb.y) - (va.y * vb.x)

    @classmethod
    def intersection(cls, a, b, c, d):
        ca = a - c ; ab = b - a ; cd = d - c

        denominator = cls.cross(cd, ab)
        if b == c: return (denominator == 0) \
                      and (cls.position(a, b, d) <= 0)

        if denominator == 0:
            colinear = (cls.cross(ca, cd) == 0)
            overlap = (cls.position(a, b, c) == 0) \
            or (cls.position(a, b, d) == 0) \
            or (cls.position(c, d, a) == 0) \
            or (cls.position(c, d, b) == 0)
            return colinear and overlap

        u = cls.cross(ca, cd) / denominator
        v = cls.cross(ca, ab) / denominator
        return (0 <= u <= 1) and (0 <= v <= 1)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self): return f"<V2({self.x}, {self.y})>"
