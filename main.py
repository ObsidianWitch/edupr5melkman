import sys
import retro
from ui import Canvas, Cursor, HList
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
canvas = Canvas(
    pos  = (0, 0),
    size = (window.rect().width, window.rect().height - 25)
)
hlist = HList(
    lst  = melkman.hull,
    pos  = canvas.rect.bottomleft,
    size = (canvas.rect.width, 25),
)

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    cursor.update()
    if events.mouse_press(retro.M_LEFT) \
       and canvas.rect.collidepoint(tuple(cursor.position)) \
    : melkman.add(cursor.position)

    # Draw
    canvas.clear()
    melkman.draw(canvas.image)
    cursor.draw(canvas.image)
    canvas.draw(window)
    hlist.draw(window)

    window.update()
