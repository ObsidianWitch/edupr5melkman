import random
import collections
from vector import V2

class SimplePolygonalChain:
    # Generates a simple polygonal chain containing `n` points and restricted
    # to `area`.
    # Complexity: O(n^2)
    @classmethod
    def generate(cls, area, n):
        lst = []
        while len(lst) < n:
            p = V2(
                random.randrange(area.x, area.width),
                random.randrange(area.y, area.height),
                index = len(lst),
            )
            if cls.verify(lst, p): lst.append(p)
        return lst

    # Given `lst`, a simple polygonal chain, verify if the property is still
    # true for `lst U {p}`.
    # Complexity: O(n)
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
    # Initializes the algorithm with a simple polygonal chain `lst`. If `lst`
    # is empty, points can be added later.
    def __init__(self, lst = []):
        self.lst = lst
        self.iter = iter(self.lst)
        self.hull = collections.deque()

    # Process the next point from `self.lst`.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(1)
    def next(self):
        def init(i = 0):
            hull = (self.lst[i + 2], self.lst[0],
                    self.lst[i + 1], self.lst[i + 2])
            self.rotation = V2.rotation(*hull[1:])
            if self.rotation == 0: init(i + 1)
            else:
                self.hull.extend(hull)
                for _ in range(i + 2): next(self.iter, None)

        p = next(self.iter, None)
        if p is None: print("finished") ; return

        # Initialize hull
        if len(self.hull) == 0: init()
        # Update hull
        else: self.step(p)


    # Add a new point `p` to `self.lst` if `self.lst U {p}` satisfies the
    # simple polygonal chain property.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(n)
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

    # Execute one step of the Melkman algorithm. Add `p` to `self.hull` if it
    # contributes to the convex hull. The `self.rotation` property must be
    # satisfied at each step of the algorithm.
    # Complexity: O(1)
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
