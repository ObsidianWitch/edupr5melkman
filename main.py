import sys
import retro
from ui import Cursor, Graphs, HList
from melkman import MelkmanMode

melkman = MelkmanMode(
    area = retro.Rect(0, 0, 800, 500),
    n    = 10,
)

window = retro.Window(
    title     = f"Melkman - {melkman.name}",
    size      = (800, 600),
    framerate = 60,
)
window.cursor(False)

events = retro.Events()
cursor = Cursor(events)
graphs = Graphs(
    melkman = melkman,
    pos     = (0, 0),
    size    = (window.rect().width, window.rect().height - 25),
)
hlist = HList(
    melkman = melkman,
    pos     = graphs.rect.bottomleft,
    size    = (graphs.rect.width, 25),
)

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    cursor.update()
    if events.key_press(retro.K_TAB):
        melkman.switch()
        retro.pygame.display.set_caption(f"Melkman - {melkman.name}")
    if events.mouse_press(retro.M_LEFT) \
       and graphs.rect.collidepoint(tuple(cursor.position)) \
    : melkman.next(cursor.position)

    # Draw
    graphs.draw(window)
    hlist.draw(window)
    cursor.draw(window)

    window.update()
