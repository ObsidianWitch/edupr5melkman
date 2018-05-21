import sys
import retro
import ui
from melkman import MelkmanMode

melkman = MelkmanMode(
    area = retro.Rect(0, 0, 800, 500),
    n    = 50,
)

window = retro.Window(
    title     = f"Melkman",
    size      = (800, 600),
    framerate = 60,
)
window.cursor(False)
events = retro.Events()
titlebar = ui.Titlebar(melkman)
cursor = ui.Cursor(events)
graphs = ui.Graphs(
    melkman = melkman,
    pos     = (0, 0),
    size    = (window.rect().width, window.rect().height - 25),
)
hlist = ui.HList(
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
       and graphs.focused(cursor.position) \
    : melkman.next(cursor.position)

    # Draw
    titlebar.draw()
    graphs.draw(window)
    hlist.draw(window)
    cursor.draw(window)

    window.update()
