import collections
import retro
from vector import V2

class Melkman:
    def __init__(self):
        self.lst = []
        self.hull = collections.deque()

    def add(self, v):
        self.lst.append(V2(v))

    def draw_points(self, image):
        font = retro.Font(18)
        for i, p in enumerate(self.lst):
            image.draw_circle(
                color  = retro.WHITE,
                center = tuple(p),
                radius = 10,
                width  = 0,
            )
            image.draw_circle(
                color  = retro.GREY,
                center = tuple(p),
                radius = 10,
                width  = 1,
            )
            txt = retro.Sprite(font.render(
                text      = str(i),
                antialias = True,
            ))
            txt.rect.center = tuple(p)
            txt.draw(image)

    def draw_lines(self, image):
        for i, _ in enumerate(self.lst[:-1]):
            p1 = self.lst[i]
            p2 = self.lst[i + 1]
            image.draw_line(
                color     = retro.BLACK,
                start_pos = tuple(p1),
                end_pos   = tuple(p2),
                width     = 1,
            )

    def draw(self, image):
        self.draw_lines(image)
        self.draw_points(image)
