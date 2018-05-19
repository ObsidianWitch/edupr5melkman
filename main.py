import sys
import retro
from cursor import Cursor
from melkman import Melkman

window = retro.Window(
    title     = "Melkman",
    size      = (800, 600),
    framerate = 60,
)
window.cursor(False)
events = retro.Events()
cursor = Cursor(events)

melkman = Melkman()

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    cursor.update()
    if events.mouse_press(retro.M_LEFT): melkman.add(cursor.position)
    if events.key_press(retro.K_SPACE): print(melkman)

    # Draw
    window.fill(retro.WHITE)
    melkman.draw(window)
    cursor.draw(window)

    window.update()
