import sys
import retro
from ui import Cursor, HList
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
hlist = HList(
    lst  = melkman.hull,
    pos  = (0, 0),
    size = (800, 25),
)

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    cursor.update()
    if events.mouse_press(retro.M_LEFT): melkman.add(cursor.position)

    # Draw
    window.fill(retro.WHITE)
    melkman.draw(window)
    cursor.draw(window)
    hlist.draw(window)

    window.update()
