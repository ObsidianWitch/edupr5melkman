import collections
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self, controller):
        self.controller = controller

        tk.Tk.__init__(self)
        self.title("Melkman")
        self.resizable(False, False)

        top_frame = tk.Frame(self)
        top_frame.grid(row = 0, column = 0, sticky = tk.W)

        button_frame = tk.Frame(top_frame)
        button_frame.grid(row = 0, column = 0, sticky = tk.W)

        # Mode buttons
        self.imode = tk.IntVar(0)
        for i, mode in enumerate(self.controller.MODES):
            mode_button = lambda mode: tk.Radiobutton(button_frame,
                text = mode.name(),
                padx = 5, pady = 5,
                indicatoron = 0,
                variable = self.imode,
                value = i,
                command = lambda: self.select(mode),
            ).grid(row = 0, column = i, sticky = tk.W)
            mode_button(mode)

        # Delete buttons
        self.del_frame = tk.Frame(button_frame)
        self.del_frame.grid(row = 0, column = 4, sticky = tk.W)
        self.del_frame.show = lambda: self.del_frame.grid(
            row = 0, column = 4, sticky = tk.W
        )
        self.del_frame.hide = self.del_frame.grid_forget
        self.del_frame.hide()

        ttk.Separator(self.del_frame, orient = tk.VERTICAL).grid(
            row = 0, column = 0,
            sticky = tk.W + tk.N + tk.S,
            padx = 10, pady = 5
        )
        tk.Button(self.del_frame,
            text    = "delete first",
            relief  = tk.RAISED,
            command = lambda: self.controller.delete(i = 0),
        ).grid(row = 0, column = 1, sticky = tk.W)
        tk.Button(self.del_frame,
            text    = "delete last",
            relief  = tk.RAISED,
            command = lambda: self.controller.delete(i = -1),
        ).grid(row = 0, column = 2, sticky = tk.W)

        self.information = Information(top_frame, controller)
        self.information.grid(row = 1, column = 0, sticky = tk.W)

        self.canvas = Canvas(self, controller)
        self.canvas.grid(row = 1, column = 0)
        self.canvas.bind("<Button-1>",
            lambda event: self.controller.next((event.x, event.y))
        )

    def select(self, mode):
        self.controller.select(mode)

        if mode == self.controller.MODES.step:
            self.del_frame.show()
        else:
            self.del_frame.hide()

    def update(self):
        self.information.update()
        self.canvas.update()
        tk.Tk.update(self)

class Information(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text = "", wraplength = 760)
        self.label.grid(row = 0, column = 0, sticky = tk.W)

    def update(self):
        txt = []

        if self.controller.checks is not None: txt.append(
            f"checks: ✓ {self.controller.passed}"
            f" / X {self.controller.failed}"
            f" / N {self.controller.CHECKS}"
        )

        txt.append(f"n: {len(self.controller.mode)}")

        def helper(melkman, i):
            hull_str = str(melkman) if melkman else "∅"
            return f"h{i}: {hull_str}"
        if self.controller.m1:
            txt.append(helper(self.controller.m1, 1))
            txt.append(helper(self.controller.m2, 2))
        else:
            txt.append(helper(self.controller.melkman, 0))

        self.label["text"] = " | ".join(txt)

class Canvas(tk.Canvas):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Canvas.__init__(self, parent,
            width  = 800,
            height = 600,
        )
        self["background"] = "white"

    def draw_circle(self, center, radius, fill, outline):
        latestp = self.controller.latestp
        radius = radius if center != latestp else radius + 2
        fill = fill[0] if center != latestp else fill[-1]
        outline = outline[0] if center != latestp else outline[-1]

        return self.create_oval(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill          = fill,
            outline       = outline,
        )

    def draw_text(self, center, text):
        return self.create_text(
            center.x, center.y,
            text       = text,
            fill       = "gray15",
        )

    def draw_edges(self, collection, color, width, dash):
        for i, _ in enumerate(collection):
            if i == len(collection) - 1: return
            p1 = collection[i]
            p2 = collection[i + 1]
            self.create_line(
                p1.x, p1.y,
                p2.x, p2.y,
                fill  = color,
                width = width,
                dash = dash,
            )

    def draw_nodes(self, collection):
        for p in collection:
            self.draw_circle(
                center     = p,
                radius     = 10,
                fill       = ("white",),
                outline    = ("firebrick2", "dark slate blue"),
            )
            self.draw_text(p, str(p.index))

    def draw_dots(self, collection):
        for p in collection:
            self.draw_circle(
                center     = p,
                radius     = 3,
                fill       = ("gray15", "dark slate blue"),
                outline    = ("gray15", "dark slate blue"),
            )

    def draw_spc_edges(self, collection):
        self.draw_edges(collection,
            color = "gray15",
            width = 1,
            dash  = (5, 5),
        )

    def draw_hull_edges(self, collection):
        self.draw_edges(collection,
            color = "firebrick2",
            width = 2,
            dash  = None,
        )

    def draw_bridges(self, m1, m2):
        if (m1 is None) or (m2 is None): return

        tangents = m1.bridge(m2)
        for t in tangents: self.draw_edges(t,
            color = "green",
            width = 2,
            dash = None,
        )

    def draw(self, melkman, spc = True, hull = True):
        if melkman is None: return
        if spc:
            self.draw_spc_edges(melkman.spc)
            self.draw_dots(melkman.spc)
        if hull:
            self.draw_hull_edges(melkman.hull)
            self.draw_nodes(melkman.hull)

    def update(self):
        self.delete("all")
        self.draw(self.controller.melkman)
        self.draw(self.controller.m1, spc = False)
        self.draw(self.controller.m2, spc = False)
        self.draw_bridges(self.controller.m1, self.controller.m2)
