import retro
from vector import V2

class Cursor:
    def __init__(self, events):
        self.events = events
        self.old_position = V2(0, 0)
        self.position = V2(0, 0)

    def update(self):
        self.position = V2(self.events.mouse_pos())
        if self.events.key_press(retro.K_LSHIFT):
            self.old_position = self.position
        if self.events.key_hold(retro.K_LSHIFT):
            rel = self.position - self.old_position
            if   abs(rel.x) < abs(rel.y): self.position.x = self.old_position.x
            elif abs(rel.x) > abs(rel.y): self.position.y = self.old_position.y

    def draw(self, image):
        def line(color, center, offset): image.draw_line(
            color = color,
            start_pos = tuple(center - offset),
            end_pos   = tuple(center + offset),
        )
        def cross(color, center, offset):
            line(color, center, V2(0, offset))
            line(color, center, V2(offset, 0))

        if self.events.key_hold(retro.K_LSHIFT): cross(
            color = retro.GREY,
            center = self.old_position,
            offset = 800
        )
        cross(color = retro.BLACK, center = self.position, offset = 5)
