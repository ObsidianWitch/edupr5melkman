import collections
import retro
from vector import V2

class SimplePolygonalChain:
    # Generates a simple polygonal chain.
    @classmethod
    def generate(cls): pass

    # Given `lst`, a simple polygonal chain, verify if the property is still
    # true for `lst U {v}`.
    @classmethod
    def verify(cls, lst, v):
        # TODO add V2.intersection classmethod
        return True

class Melkman:
    def __init__(self):
        self.lst = []
        self.hull = collections.deque()

    # Adds a new point `p` to `self.lst` if {`p`} U `self.lst` satisfies the
    # simple polygonal chain property. Then, apply the Melkman algorithm to
    # decide whether to add this point to `self.hull` or not.
    def add(self, p):
        v = V2(p, index = len(self.lst))

        # Initialize counter-clockwise hull
        if len(self.lst) < 2:
            self.lst.append(v)
        elif len(self.lst) == 2:
            self.lst.append(v)
            rotation = V2.position(*self.lst)
            if rotation < 0: # counter-clockwise -> 3213
                self.hull.extend(self.lst[::-1])
                self.hull.append(self.lst[-1])
            else: # clockwise or colinear -> 3123
                self.hull.append(self.lst[-1])
                self.hull.extend(self.lst)
        # Update hull
        elif SimplePolygonalChain.verify(self.lst, v):
            self.lst.append(v)
            self.step(v)

    def step(self, v):
        def right_start(): return V2.position(
            self.hull[0], self.hull[1], v
        ) >= 0
        def right_end(): return V2.position(
            self.hull[-2], self.hull[-1], v
        ) >= 0

        if right_start() and right_end(): return
        while not right_start(): self.hull.popleft()
        while not right_end(): self.hull.pop()

        self.hull.appendleft(v)
        self.hull.append(v)

    def draw_points(self, collection, image, simple):
        for v in collection:
            if not simple: image.draw_circle(
                color  = retro.WHITE,
                center = tuple(v),
                radius = 10,
                width  = 0,
            )
            image.draw_circle(
                color  = retro.BLACK if simple else retro.RED,
                center = tuple(v),
                radius = 2 if simple else 10,
                width  = 0 if simple else 1,
            )
            if not simple:
                txt = retro.Sprite(retro.Font(18).render(
                    text      = str(v.index),
                    color     = retro.RED,
                    antialias = True,
                ))
                txt.rect.center = tuple(v)
                txt.draw(image)

    def draw_lines(self, collection, image, color):
        for i, _ in enumerate(collection):
            if i == len(collection) - 1: return
            v1 = collection[i]
            v2 = collection[i + 1]
            image.draw_line(
                color     = color,
                start_pos = tuple(v1),
                end_pos   = tuple(v2),
                width     = 1,
            )

    def draw(self, image):
        self.draw_points(self.lst, image, True)
        self.draw_lines(self.lst, image, retro.BLACK)
        self.draw_points(self.hull, image, False)
        self.draw_lines(self.hull, image, retro.RED)

    def __repr__(self): return " ".join(
        str(v.index) for v in self.hull
    )
