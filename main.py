import sys
import retro
from melkman import Melkman

window = retro.Window(
    title     = "Melkman",
    size      = (800, 600),
    framerate = 20,
)
events = retro.Events()

melkman = Melkman()

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if events.mouse_press(retro.M_LEFT):
        melkman.add(events.mouse_pos())

    # Draw
    window.fill(retro.WHITE)
    melkman.draw(window)

    window.update()
