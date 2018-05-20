import retro
from vector import V2

class Canvas(retro.Sprite):
    def __init__(self, pos, size):
        retro.Sprite.__init__(self, retro.Image(size))

    def clear(self):
        self.image.fill(retro.WHITE)

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

class HList(retro.Sprite):
    def __init__(self, lst, pos, size):
        self.lst = lst
        retro.Sprite.__init__(self, retro.Image(size))
        self.rect.topleft = pos

    def draw(self, image):
        def draw_rect(rect): self.image.draw_rect(
            color = retro.GREY, rect = rect, width = 1
        )

        self.image.fill(retro.WHITE)
        draw_rect(retro.Rect(0, 0, *self.rect.size))
        for i, p in enumerate(self.lst):
            rect = retro.Rect(0, 0, self.rect.height, self.rect.height)
            rect.x += i * self.rect.height
            draw_rect(rect)

            txt = retro.Sprite(retro.Font(int(self.rect.height)).render(
                text      = str(p.index),
                color     = retro.BLACK,
                antialias = True,
            ))
            txt.rect.center = rect.center
            txt.draw(self.image)
        retro.Sprite.draw(self, image)
