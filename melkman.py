import random
import collections
import itertools
from vector import V2

class Mode:
    def __init__(self, area):
        self.area = area
        self.latestp = None

    @property
    def lst(self): return self.instance.lst

    @property
    def hull(self): return self.instance.hull

class InteractiveMode(Mode):
    def __init__(self, area):
        Mode.__init__(self, area)
        self.instance = Melkman([])

    @property
    def name(self): return "interactive"

    @property
    def finished(self): return False

    def next(self, p):
        self.latestp = self.instance.add(p)

class StepMode(Mode):
    NPOINTS = 100

    def __init__(self, area):
        Mode.__init__(self, area)
        self.instance = Melkman(
            SimplePolygonalChain.generate(self.area, self.NPOINTS)
        )

    @property
    def name(self): return "step"

    @property
    def finished(self): return (
        self.hull
        and (not self.latestp)
    )

    def next(self, *args):
        self.latestp = self.instance.next()

class TestMode(Mode):
    NPOINTS = 250
    CHECKS  = 5000

    def __init__(self, area):
        Mode.__init__(self, area)
        self.passed  = 0
        self.failed  = 0
        self.instance = None

    @property
    def name(self): return "test"

    @property
    def checks(self): return self.passed + self.failed

    @property
    def finished(self): return self.checks >= self.CHECKS

    def next(self, *args):
        while self.checks < self.CHECKS:
            self.instance = Melkman(
                SimplePolygonalChain.generate(self.area, self.NPOINTS)
            )
            self.instance.run()
            if self.instance.check(): self.passed += 1
            else: self.failed += 1 ; break
            print(self.passed, self.failed)

# Proxy class for Melkman allowing to switch between modes.
# * Interactive: points are added individually to the simple polygonal chain.
# * Step: a simple polygonal chain is generated.
# * Test: algorithm robustness test.
class ModeSwitcher:
    def __init__(self, area):
        self.modes = itertools.cycle((InteractiveMode, StepMode, TestMode))
        self.mode = next(self.modes)(area)
        self.area = area

    @property
    def name(self): return self.mode.name

    @property
    def finished(self): return self.mode.finished

    @property
    def latestp(self): return self.mode.latestp

    @property
    def lst(self): return self.mode.instance.lst if self.mode.instance \
                     else ()

    @property
    def hull(self): return self.mode.instance.hull if self.mode.instance \
                     else ()

    def switch(self):
        self.mode = next(self.modes)(self.area)

    def next(self, p): self.mode.next(p)

class SimplePolygonalChain:
    # Generate a simple polygonal chain containing at most `n` points and
    # restricted to `area`.
    # Complexity: O(n^2)
    @classmethod
    def generate(cls, area, n):
        lst = []
        for _ in range(n):
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
            if V2.intersection(
                a = lst[i],  b = lst[i + 1],
                c = lst[-1], d = p,
            ): return False
        return True

class Melkman:
    # Initializes the algorithm with a simple polygonal chain `lst`. If `lst`
    # is empty, points can be added later.
    def __init__(self, lst):
        self.lst = lst
        self.iter = iter(self.lst)
        self.hull = collections.deque()

    # Process all points from `self.lst`.
    # Complexity: O(n)
    def run(self):
        while self.next(): pass

    # Process the next point from `self.lst`.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Returns the latest processed point.
    # Complexity: O(1)
    def next(self):
        def init(i = 0):
            hull = (self.lst[i + 2], self.lst[0],
                    self.lst[i + 1], self.lst[i + 2])
            self.rotation = V2.rotation(*hull[1:])
            if self.rotation == 0: return init(i + 1)
            else:
                self.hull.extend(hull)
                for _ in range(i + 3): next(self.iter, None)
                return self.hull[-1]

        # Initialize hull
        if len(self.hull) == 0: return init()

        # Update hull
        p = next(self.iter, None)
        if p is None: return # finished
        self.step(p)

        return p

    # Add a new point `p` to `self.lst` if `self.lst U {p}` satisfies the
    # simple polygonal chain property.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Returns the latest processed point.
    # Complexity: O(n)
    def add(self, p):
        def init(p):
            self.lst.append(p)
            if len(self.lst) < 3: return
            hull = (self.lst[-1], self.lst[0], self.lst[-2], self.lst[-1])
            self.rotation = V2.rotation(*hull[1:])
            if self.rotation == 0: return # collinear
            self.hull.extend(hull)

        p = V2(p, index = len(self.lst))
        if not SimplePolygonalChain.verify(self.lst, p): return

        # Initialize hull
        if len(self.hull) == 0: init(p)
        # Update hull
        else:
            self.lst.append(p)
            self.step(p)

        return self.lst[-1]

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

    # Once the algorithm has processed the whole `self.lst`, this method can
    # check the validity of the convex hull.
    # 1. Check the rotation stays the same for the whole hull.
    # 2. For each edge [AB] in the hull, for every point [P] from `self.lst`,
    #    check that the rotation for (A, B, P) is equal to `self.rotation` or 0
    #    (colinear). It means that each point must be inside or on the hull.
    # Note: by verifying the second property, we also verify the first one.
    def check(self):
        for i, _ in enumerate(self.hull):
            if i == len(self.hull) - 1: break # NB deque cannot be sliced
            a = self.hull[i]
            b = self.hull[i + 1]
            for p in self.lst:
                r = V2.rotation(a, b, p)
                if (r != self.rotation) and (r != 0): return False
        return True
