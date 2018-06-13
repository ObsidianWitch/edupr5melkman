import collections
import itertools
from utils import Table, Iter
from vector import V2
from spc import SimplePolygonalChain as SPC

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
        self.rotation = 0
        self.history = History()

    @property
    def initialized(self): return (len(self.hull) >= 4) \
                              and (self.rotation != 0)

    def init(self):
        p = self.iter.current
        if self.hull:
            self.history.new()
            self.history.insert(
                side  = -1,
                point = self.hull.popleft(),
            )
        self.hull.appendleft(p)
        self.hull.append(p)
        if len(self.hull) < 4: return

        self.rotation = V2.rotation(
            self.hull[1], self.hull[-2], self.hull[-1]
        )

    # Process all points from `self.lst`.
    # Complexity: O(n)
    def run(self):
        while not self.iter.finished: self.next()

    # Process the next point from `self.lst`.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(1)
    def next(self):
        if self.iter.finished: return
        p = self.iter.next()

        # Initialize hull
        if not self.initialized: return self.init()
        # Update hull
        elif p is not None: self.step(p)

    # Add a new point `p` to `self.lst` if `self.lst U {p}` satisfies the
    # simple polygonal chain property.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(n)
    def add(self, p):
        p = V2(p, index = len(self.lst))
        if not SPC.check_1(self.lst, p): return
        self.lst.append(p)
        self.iter.next()

        # Initialize hull
        if not self.initialized: return self.init()
        # Update hull
        else: self.step(p)

    # Delete a point from `self.lst`. It can only be deleted if `self.lst \ {p}`
    # is a simple polygonal chain. If p is at one end of `self.lst`, we can
    # remove it without reverifying the simple polygonal chain property. If `p`
    # is successfully removed, recompute the convex hull.
    def delete(self, i):
        def at_end(): return (i == 0 or i == len(self.lst) - 1 or i == -1)
        def is_spc(): return SPC.check_n(
            self.lst[0 : i], self.lst[i + 1 :]
        )

        if not self.lst: return
        p = self.lst[i]

        # check simple polygonal chain
        if (not at_end()) and (not is_spc()): return
        del self.lst[i]

        # update indices
        for j, p in enumerate(self.lst): p.index = j

        # recompute convex hull
        self.__init__(self.lst) # reset
        self.run()

    def rewind(self):
        actions = self.history.rewind() or ()
        self.iter.prev()
        if actions or (len(self.hull) == 2):
            self.hull.pop()
            self.hull.popleft()

        for a in actions[::-1]:
            if   a.side == -1: self.hull.appendleft(a.point)
            elif a.side ==  1: self.hull.append(a.point)

    # TODO doc
    def split(self):
        cls = self.__class__
        m1 = cls(self.iter.remaining())
        m2 = cls(self.iter.processed(reverse = True))
        m2.run()
        return m1, m2

    # TODO use
    # TODO doc
    # brute force method
    # given 2 convex hulls of respective size l and m
    # complexity: o(l^2 + m^2)
    def bridge(self, other):
        h1, h2 = self.hull, other
        def is_tangent(a, b):
            side = 0
            for p in itertools.chain(h1, h2):
                rot_abp = V2.rotation(a, b, p)
                if side == 0: side = rot_abp
                elif (rot_abp != side) and (rot_abp != 0): return False
            return True

        tangents = []
        for a, b in itertools.product(h1, h2):
            if is_tangent(a, b): tangents.append((a, b))
            if len(tangents) >= 2: break
        return tangents

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

    def __repr__(self): return " ".join(
        str(p.index) for p in self.hull
    )
