import sys
import retro
from ui import Cursor, Graphs, HList
from melkman import Melkman

melkman = Melkman()

window = retro.Window(
    title     = "Melkman",
    size      = (800, 600),
    framerate = 60,
)
window.cursor(False)
events = retro.Events()
cursor = Cursor(events)
graphs = Graphs(
    lst  = melkman.lst,
    hull = melkman.hull,
    pos  = (0, 0),
    size = (window.rect().width, window.rect().height - 25),
)
hlist = HList(
    lst  = melkman.hull,
    pos  = graphs.rect.bottomleft,
    size = (graphs.rect.width, 25),
)

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    cursor.update()
    if events.mouse_press(retro.M_LEFT) \
       and graphs.rect.collidepoint(tuple(cursor.position)) \
    : melkman.add(cursor.position)

    # Draw
    graphs.draw(window)
    hlist.draw(window)
    cursor.draw(window)

    window.update()
