import retro
import ui
from melkman import MelkmanMode

melkman = MelkmanMode(
    area = retro.Rect(0, 0, 800, 500),
    n    = 50,
)

window = ui.Window(
    title     = f"Melkman",
    size      = (800, 600),
    framerate = 60,
)
titlebar = ui.Titlebar(melkman)
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
window.widgets.extend((titlebar, graphs, hlist))
window.update_buffer()

def main():
    if window.events.key_press(retro.K_TAB):
        melkman.switch()
        window.update_buffer()

    if window.events.mouse_press(retro.M_LEFT) \
       and graphs.focused(window.cursor.position) \
    :
        melkman.next(window.cursor.position)
        window.update_buffer()

window.loop(main)
