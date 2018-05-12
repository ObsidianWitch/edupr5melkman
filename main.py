import sys
import retro
from hull import Hull

window = retro.Window(
    title     = "Melkman",
    size      = (800, 600),
    framerate = 60,
)
events = retro.Events()

hull = Hull()

while 1:
    # Update
    events.update()
    if events.event(retro.QUIT): sys.exit()

    if events.mouse_press(retro.M_LEFT):
        hull.add(events.mouse_pos())

    # Draw
    window.fill(retro.WHITE)
    hull.draw(window)

    window.update()
