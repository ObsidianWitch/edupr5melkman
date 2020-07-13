import random
from vector import V2

class SimplePolygonalChain:
    # Generate a simple polygonal chain containing at most `n` points and
    # restricted to `area`.
    # Complexity: O(n^2)
    @classmethod
    def generate(cls, area, n):
        spc = []
        for _ in range(n):
            p = V2(
                random.randrange(area.x, area.width),
                random.randrange(area.y, area.height),
                index = len(spc),
            )
            if cls.check_1(spc, p): spc.append(p)
        return spc

    # Given `spc`, a simple polygonal chain, check if the property is still
    # true for `spc U {p}`.
    # Complexity: O(n)
    @classmethod
    def check_1(cls, spc, p):
        if len(spc) <= 1: return True
        for i, _ in enumerate(spc):
            if i == len(spc) - 1: break
            if V2.intersection(
                a = spc[i],  b = spc[i + 1],
                c = spc[-1], d = p,
            ): return False
        return True
