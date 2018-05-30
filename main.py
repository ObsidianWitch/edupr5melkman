import types
import melkman
import ui

melkman = melkman.ModePicker(
    area = types.SimpleNamespace(
        x = 0, y = 0,
        width = 800, height = 600,
    ),
)
window = ui.Window(melkman)
window.mainloop()
