import retro
from vector import V2

class Hull:
    def __init__(self):
        self.lst = []

    def add(self, v):
        self.lst.append(V2(v))

    def draw(self, image):
        for p in self.lst: image.draw_circle(
            color  = retro.GREY,
            center = tuple(p),
            radius = 10,
            width  = 1,
        )
        for i, _ in enumerate(self.lst[:-1]):
            p1 = self.lst[i]
            p2 = self.lst[i + 1]
            image.draw_line(
                color     = retro.BLACK,
                start_pos = tuple(p1),
                end_pos   = tuple(p2),
                width     = 1,
            )
