import collections
import itertools
from utils import Table, Iter
from vector import V2
from spc import SimplePolygonalChain as SPC

class History(collections.deque):
    def __init__(self): collections.deque.__init__(self)

    # Add a new history entry.
    def new(self, index): self.append(Table(
        index = index - 1,
        left  = [],
        right = [],
    ))

    # Add a point `p` to the current entry. `p` has been popped from the left
    # of a deque.
    def insert_left(self, p): self[-1].left.append(p)

    # Add a point `p` to the current entry. `p` has been popped from the right
    # of a deque.
    def insert_right(self, p): self[-1].right.append(p)

    def rewind(self): return self.pop() if self else None

class Melkman:
    # Initializes the algorithm with a simple polygonal chain `spc`. If `spc`
    # is empty, points can be added later.
    def __init__(self, spc):
        self.spc = spc
        self.iter = Iter(self.spc)
        self.hull = collections.deque()
        self.rotation = 0
        self.history = History()

    @property
    def initialized(self): return (len(self.hull) >= 4) \
                              and (self.rotation != 0)

    # TODO fix
    def init(self, p):
        def popl(): self.history.insert_left(self.hull.popleft())
        def popr(): self.history.insert_right(self.hull.pop())

        self.rotation = V2.rotation(
            self.hull[1], self.hull[-1], p
        ) if len(self.hull) >= 2 else 0

        self.history.new(index = self.iter.i)
        if (len(self.hull) >= 3) and (self.rotation == 0): popr()
        if self.hull: popl()
        self.hull.appendleft(p)
        self.hull.append(p)

    # Process all points from `self.spc`.
    # Complexity: O(n)
    def run(self):
        while not self.iter.finished: self.next()

    # Process the next point from `self.spc`.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(1)
    def next(self):
        if self.iter.finished: return
        p = self.iter.next()

        if not self.initialized: return self.init(p)
        else: self.step(p)

    # Add a new point `p` to `self.spc` if `self.spc U {p}` satisfies the
    # simple polygonal chain property.
    # Then, execute one step of the Melkman algorithm to decide whether to add
    # this point to `self.hull` or not.
    # Complexity: O(n)
    def add(self, p):
        p = V2(p, index = len(self.spc))
        if not SPC.check_1(self.spc, p): return
        self.spc.append(p)
        self.iter.next()

        if not self.initialized: return self.init(p)
        else: self.step(p)

    # Delete a point from `self.spc`. It can only be deleted if `self.spc \ {p}`
    # is a simple polygonal chain. If p is at one end of `self.spc`, we can
    # remove it without reverifying the simple polygonal chain property. If `p`
    # is successfully removed, recompute the convex hull.
    def delete(self, i):
        def at_end(): return (i == 0 or i == len(self.spc) - 1 or i == -1)
        def is_spc(): return SPC.check_n(
            self.spc[0 : i], self.spc[i + 1 :]
        )

        if not self.spc: return
        p = self.spc[i]

        # check simple polygonal chain
        if (not at_end()) and (not is_spc()): return
        del self.spc[i]

        # update indices
        for j, p in enumerate(self.spc): p.index = j

        # recompute convex hull
        self.__init__(self.spc) # reset
        self.run()

    def rewind(self):
        actions = self.history.rewind()
        if not actions: return

        self.iter.i = actions.index
        self.hull.pop()
        self.hull.popleft()
        for p in actions.left[::-1]:  self.hull.appendleft(p)
        for p in actions.right[::-1]: self.hull.append(p)

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
        h1, h2 = self.hull, other.hull
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

        if rotstart() and rotend(): return
        self.history.new(index = self.iter.i)
        while not rotstart(): self.history.insert_left(
            self.hull.popleft()
        )
        while not rotend(): self.history.insert_right(
            self.hull.pop(),
        )

        self.hull.appendleft(p)
        self.hull.append(p)

    # Once the algorithm has processed the whole `self.spc`, this method can
    # check the validity of the convex hull.
    # For each edge [AB] in the hull, for every point P from `self.spc`,
    # check that the rotation for (A, B, P) is equal to `self.rotation` or 0
    # (colinear). It means that each point must be inside or on the hull.
    def check(self):
        # NB deque does not allow slice notation
        for i in range(len(self.hull) - 1):
            a = self.hull[i]
            b = self.hull[i + 1]
            for p in self.spc:
                r = V2.rotation(a, b, p)
                if (r != self.rotation) and (r != 0): return False
        return True

    def __repr__(self): return ", ".join(
        str(p.index) for p in self.hull
    ) if self.hull else "∅"
