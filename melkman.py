import collections
import retro
from vector import V2

class SimplePolygonalChain:
    # Generates a simple polygonal chain.
    @classmethod
    def generate(cls): pass

    # Given `lst`, a simple polygonal chain, verify if the property is still
    # true for `lst U {p}`.
    @classmethod
    def verify(cls, lst, p):
        if len(lst) <= 1: return True
        for i, _ in enumerate(lst):
            if i == len(lst) - 1: break
            va = lst[i+1] - lst[i]
            if V2.intersection(
                a = lst[i],  b = lst[i + 1],
                c = lst[-1], d = p,
            ): return False
        return True

class Melkman:
    def __init__(self):
        self.lst = []
        self.hull = collections.deque()

    # Adds a new point `p` to `self.lst` if {`p`} U `self.lst` satisfies the
    # simple polygonal chain property. Then, apply the Melkman algorithm to
    # decide whether to add this point to `self.hull` or not.
    def add(self, p):
        p = V2(p, index = len(self.lst))
        if not SimplePolygonalChain.verify(self.lst, p): return

        # Initialize hull
        if len(self.hull) == 0:
            self.lst.append(p)
            if len(self.lst) < 3: return
            hull = (self.lst[-1], self.lst[0], self.lst[-2], self.lst[-1])
            self.rotation = V2.rotation(*hull[1:])
            if self.rotation == 0: return # collinear
            self.hull.extend(hull)
        # Update hull
        else:
            self.lst.append(p)
            self.step(p)

    def step(self, p):
        def rotstart(): return V2.rotation(
            self.hull[0], self.hull[1], p
        ) == self.rotation
        def rotend(): return V2.rotation(
            self.hull[-2], self.hull[-1], p
        ) == self.rotation

        if rotstart() and rotend(): return
        while not rotstart(): self.hull.popleft()
        while not rotend(): self.hull.pop()

        self.hull.appendleft(p)
        self.hull.append(p)

    def __repr__(self): return " ".join(
        str(p.index) for p in self.hull
    )
