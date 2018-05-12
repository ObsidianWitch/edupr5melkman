import sys
import retro

window = retro.Window(
    title     = "Melkman",
    size      = (800, 600),
    framerate = 60,
)
events = retro.Events()

while 1:
    events.update()
    if events.event(retro.QUIT): sys.exit()

    # Update
    # TODO

    # Draw
    window.fill(retro.WHITE)

    window.update()
