import random
import collections
from utils import Table, Iter
from vector import V2

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
            if cls.check_1(lst, p): lst.append(p)
        return lst

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

    # Given two simple polygonal chains, check if the property is still true
    # for `spc1 U spc2`.
    # The test is equivalent to the following:
    # with `a = spc1[-1]` and `b = spc2[0]`, check the [ab] line segment
    # against all line segments from `spc1` and `spc2`.
    # Complexity: O(n)
    @classmethod
    def check_n(cls, spc1, spc2):
        return cls.check_1(spc1, spc2[0]) \
           and cls.check_1(spc2[::-1], spc1[-1])

class History(collections.deque):
    def __init__(self): collections.deque.__init__(self)

    # Add a new history entry.
    def new(self): self.append([])

    # Adds a new element to the latest entry. We save the `point` and the `side`
    # where this elements was when it was poped from its deque (-1 for left or
    # 1 for right).
    def insert(self, side, point): self[-1].append(Table(
        side  = side,
        point = point,
    ))

    def rewind(self):
        if self: return self.pop()

class Melkman:
    # Initializes the algorithm with a simple polygonal chain `lst`. If `lst`
    # is empty, points can be added later.
    def __init__(self, lst):
        self.lst = lst
        self.iter = Iter(self.lst)
        self.hull = collections.deque()
        self.history = History()

    # Process all points from `self.lst`.
    # Complexity: O(n)
    def run(self):
        while not self.iter.finished: self.next()

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
                self.iter.i = i + 2

        # Initialize hull
        if len(self.hull) == 0: return init()

        # Update hull
        p = self.iter.next()
        if p is None: return # finished
        self.step(p)

    # Add a new point `p` to `self.lst` if `self.lst U {p}` satisfies the
    # simple polygonal chain property.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
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
        if not SimplePolygonalChain.check_1(self.lst, p): return

        # Initialize hull
        if len(self.hull) == 0: init(p)
        # Update hull
        else:
            self.lst.append(p)
            self.step(p)

        self.iter.next()

    # Delete a point from `self.lst`. It can only be deleted if `self.lst \ {p}`
    # is a simple polygonal chain. If p is at one end of `self.lst`, we can
    # remove it without reverifying the simple polygonal chain property. If `p`
    # is successfully removed, recompute the convex hull.
    def delete(self, i):
        def at_end(): return (i == 0 or i == len(self.lst) - 1 or i == -1)
        def is_spc(): return SimplePolygonalChain.check_n(
            self.lst[0 : i], self.lst[i + 1 :]
        )

        p = self.lst[i]

        # check simple polygonal chain
        if (not at_end()) and (not is_spc()): return
        del self.lst[i]

        # update indices
        for j, p in enumerate(self.lst): p.index = j

        # recompute convex hull
        self.iter = Iter(self.lst)
        self.hull = collections.deque()
        if len(self.lst) >= 3: self.run()

    def rewind(self):
        actions = self.history.rewind()
        # if not actions: return self.iter.prev() if self.history else None
        if not actions: return self.iter.prev()
        self.hull.pop()
        self.hull.popleft()
        self.iter.prev()
        for a in actions[::-1]:
            if   a.side == -1: self.hull.appendleft(a.point)
            elif a.side ==  1: self.hull.append(a.point)

    # Execute one step of the Melkman algorithm. Add `p` to `self.hull` if it
    # contributes to the convex hull. The `self.rotation` property must be
    # satisfied at each step of the algorithm.
    # Deleted points are saved in `self.history`.
    # Complexity: O(1)
    def step(self, p):
        def rotstart(): return V2.rotation(
            self.hull[0], self.hull[1], p
        ) == self.rotation
        def rotend(): return V2.rotation(
            self.hull[-2], self.hull[-1], p
        ) == self.rotation

        self.history.append([])
        if rotstart() and rotend(): return
        while not rotstart(): self.history.insert(
            side  = -1,
            point = self.hull.popleft(),
        )
        while not rotend(): self.history.insert(
            side  = 1,
            point = self.hull.pop(),
        )

        self.hull.appendleft(p)
        self.hull.append(p)

    def __repr__(self): return " ".join(
        str(p.index) for p in self.hull
    )

    # Once the algorithm has processed the whole `self.lst`, this method can
    # check the validity of the convex hull.
    # For each edge [AB] in the hull, for every point P from `self.lst`,
    # check that the rotation for (A, B, P) is equal to `self.rotation` or 0
    # (colinear). It means that each point must be inside or on the hull.
    def check(self):
        # NB deque does not allow slice notation
        for i in range(len(self.hull) - 1):
            a = self.hull[i]
            b = self.hull[i + 1]
            for p in self.lst:
                r = V2.rotation(a, b, p)
                if (r != self.rotation) and (r != 0): return False
        return True
