import collections
import tkinter as tk

class Window(tk.Tk):
    def __init__(self, controller):
        self.controller = controller

        tk.Tk.__init__(self)
        self.title("Melkman")
        self.resizable(False, False)

        top_frame = tk.Frame(self)
        top_frame.grid(row = 0, column = 0, sticky = tk.W)

        new_menu = tk.Menubutton(top_frame,
            text   = "New",
            relief = tk.RAISED
        )
        new_menu.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.E + tk.W)
        new_menu.menu = tk.Menu(new_menu)
        new_menu["menu"] = new_menu.menu
        for i, mode in enumerate(self.controller.MODES):
            add_mode = lambda mode: new_menu.menu.add_command(
                label   = mode.name(),
                command = lambda: self.select(mode),
            ) ; add_mode(mode)

        self.del_menu = tk.Menubutton(top_frame,
            text   = "Del",
            relief = tk.RAISED
        )
        self.del_menu.show = lambda: self.del_menu.grid(
            row = 0, column = 1, sticky = tk.N + tk.S + tk.E + tk.W
        )
        self.del_menu.show()
        self.del_menu.menu = tk.Menu(self.del_menu)
        self.del_menu["menu"] = self.del_menu.menu
        self.del_menu.menu.add_command(
            label   = "first",
            command = lambda: self.controller.delete(i = 0),
        )
        self.del_menu.menu.add_command(
            label   = "last",
            command = lambda: self.controller.delete(i = -1),
        )

        self.information = Information(top_frame, controller)
        self.information.grid(row = 0, column = 2, sticky = tk.W)

        self.canvas = Canvas(self, controller)
        self.canvas.grid(row = 1, column = 0)
        self.canvas.bind("<Button-1>",
            lambda event: self.controller.next((event.x, event.y))
        )

    def select(self, mode):
        self.controller.select(mode)

        if mode == self.controller.MODES.test:
            self.del_menu.grid_forget()
        else:
            self.del_menu.show()

    def update(self):
        self.information.update()
        self.canvas.update()
        tk.Tk.update(self)

class Information(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.state_label = tk.Label(self,
            text = ""
        )
        self.state_label.grid(row = 0, column = 0, sticky = tk.W)

        self.hull_label = tk.Label(self,
            text = "",
            wraplength = 760,
            justify = tk.LEFT,
        )
        self.hull_label.grid(row = 1, column = 0, sticky = tk.W)

    def update_state(self):
        txt = []
        txt.append(f"Mode: {self.controller.mode.name()}")

        txt.append(f"Points: {len(self.controller.mode)}")

        if self.controller.checks is not None: txt.append(
            f"Checks: ✓ {self.controller.passed}"
            f" / X {self.controller.failed}"
            f" / N {self.controller.CHECKS}"
        )

        if self.controller.finished: txt.append("finished")

        self.state_label["text"] = " | ".join(txt)

    def hull_str(self, melkman):
        if not hull: return "∅"
        else: return melkman

    def update_hulls(self):
        def helper(melkman, i):
            hull_str = str(melkman) if melkman else "∅"
            return f"h{i}: {hull_str}"

        self.hull_label["text"] = "\n".join((
            helper(self.controller.m1, 1),
            helper(self.controller.m2, 2)
        )) if self.controller.m1 else helper(self.controller.melkman, 0)

    def update(self):
        self.update_hulls()
        self.update_state()

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
            activefill    = "light slate blue",
            outline       = outline,
            activeoutline = "light slate blue",
        )

    def draw_text(self, center, text):
        return self.create_text(
            center.x, center.y,
            text       = text,
            fill       = "gray15",
            activefill = "light slate blue"
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

    # Bind events to multiple items.
    # * Right click: remove the point associated with the items.
    def bind_items(self, p, *ids):
        for id in ids:
            self.tag_bind(id, "<Button-3>",
                lambda *args: self.controller.delete(p)
            )

    def draw_nodes(self, collection):
        for p in collection:
            id1 = self.draw_circle(
                center     = p,
                radius     = 10,
                fill       = ("white",),
                outline    = ("firebrick2", "dark slate blue"),
            )
            id2 = self.draw_text(p, str(p.index))
            self.bind_items(p, id1, id2)

    def draw_dots(self, collection):
        for p in collection:
            id = self.draw_circle(
                center     = p,
                radius     = 3,
                fill       = ("gray15", "dark slate blue"),
                outline    = ("gray15", "dark slate blue"),
            )
            self.bind_items(p, id)

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
        tangents = m1.bridge(m2)
        for t in tangents: self.draw_edges(t,
            color = "green",
            width = 2,
            dash = None,
        )

    def draw(self, *instances):
        for i, melkman in enumerate(instances):
            if melkman is None: return
            if i == 0: self.draw_spc_edges(melkman.spc)
            if i == 0: self.draw_dots(melkman.spc)
            if i == 1: self.draw_bridges(instances[1], instances[2])
            self.draw_hull_edges(melkman.hull)
            self.draw_nodes(melkman.hull)

    def update(self):
        self.delete("all")
        self.draw(
            self.controller.melkman,
            self.controller.m1,
            self.controller.m2
        )
