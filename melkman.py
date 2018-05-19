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
            self.rotation = V2.rotation(*self.lst)
            # TODO check collinearity
            self.hull.append(self.lst[-1])
            self.hull.extend(self.lst)
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

    def draw_points(self, collection, image, simple):
        for p in collection:
            if not simple: image.draw_circle(
                color  = retro.WHITE,
                center = tuple(p),
                radius = 10,
                width  = 0,
            )
            image.draw_circle(
                color  = retro.BLACK if simple else retro.RED,
                center = tuple(p),
                radius = 2 if simple else 10,
                width  = 0 if simple else 1,
            )
            if not simple:
                txt = retro.Sprite(retro.Font(18).render(
                    text      = str(p.index),
                    color     = retro.RED,
                    antialias = True,
                ))
                txt.rect.center = tuple(p)
                txt.draw(image)

    def draw_lines(self, collection, image, color):
        for i, _ in enumerate(collection):
            if i == len(collection) - 1: return
            p1 = collection[i]
            p2 = collection[i + 1]
            image.draw_line(
                color     = color,
                start_pos = tuple(p1),
                end_pos   = tuple(p2),
                width     = 1,
            )

    def draw(self, image):
        self.draw_points(self.lst, image, True)
        self.draw_lines(self.lst, image, retro.BLACK)
        self.draw_points(self.hull, image, False)
        self.draw_lines(self.hull, image, retro.RED)

    def __repr__(self): return " ".join(
        str(p.index) for p in self.hull
    )
