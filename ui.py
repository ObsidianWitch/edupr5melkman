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

class Graphs:
    def __init__(self, melkman, pos, size):
        self.melkman = melkman
        retro.Sprite.__init__(self, retro.Image(size))
        self.rect.topleft = pos

    def draw_circle(self, bg_color, border_color, center, radius, width):
        self.image.draw_circle(bg_color, center, radius, 0)
        self.image.draw_circle(border_color, center, radius, width)

    def draw_nodes(self, collection):
        for p in collection:
            self.draw_circle(
                bg_color     = retro.WHITE,
                border_color = retro.RED,
                center       = tuple(p),
                radius       = 10,
                width        = 1,
            )

            txt = retro.Sprite(retro.Font(18).render(
                text      = str(p.index),
                color     = retro.RED,
                antialias = True,
            ))
            txt.rect.center = tuple(p)
            txt.draw(self.image)

    def draw_dots(self, collection):
        for p in collection:
            self.image.draw_circle(
                color  = retro.BLACK,
                center = tuple(p),
                radius = 2,
                width  = 0,
            )

    def draw_edges(self, collection, color):
        for i, _ in enumerate(collection):
            if i == len(collection) - 1: return
            p1 = collection[i]
            p2 = collection[i + 1]
            self.image.draw_line(
                color     = color,
                start_pos = tuple(p1),
                end_pos   = tuple(p2),
                width     = 1,
            )

    def draw(self, image):
        self.image.fill(retro.WHITE)
        self.draw_dots(self.melkman.lst)
        self.draw_edges(self.melkman.lst, retro.BLACK)
        self.draw_nodes(self.melkman.hull)
        self.draw_edges(self.melkman.hull, retro.RED)
        retro.Sprite.draw(self, image)

class HList(retro.Sprite):
    def __init__(self, melkman, pos, size):
        self.melkman = melkman
        retro.Sprite.__init__(self, retro.Image(size))
        self.rect.topleft = pos

    def draw(self, image):
        def draw_rect(rect): self.image.draw_rect(
            color = retro.GREY, rect = rect, width = 1
        )

        self.image.fill(retro.WHITE)
        draw_rect(retro.Rect(0, 0, *self.rect.size))
        for i, p in enumerate(self.melkman.hull):
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
