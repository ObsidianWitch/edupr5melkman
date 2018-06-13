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
                label   = mode.NAME,
                command = lambda: self.controller.select(mode),
            ) ; add_mode(mode)

        del_menu = tk.Menubutton(top_frame,
            text   = "Del",
            relief = tk.RAISED
        )
        del_menu.grid(row = 0, column = 1, sticky = tk.N + tk.S + tk.E + tk.W)
        del_menu.menu = tk.Menu(del_menu)
        del_menu["menu"] = del_menu.menu
        del_menu.menu.add_command(
            label   = "first",
            command = lambda: self.controller.delete(i = 0),
        )
        del_menu.menu.add_command(
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
        txt.append(f"Mode: {self.controller.NAME}")

        txt.append(f"Points: {len(self.controller.mode)}")

        if self.controller.checks is not None: txt.append(
            f"Checks: ✓ {self.controller.passed}"
            f" / X {self.controller.failed}"
            f" / N {self.controller.CHECKS}"
        )

        if self.controller.finished: txt.append("finished")

        self.state_label["text"] = " | ".join(txt)

    def hull_str(self, hull):
        if not hull: return "∅"
        else: return  ", ".join(
            str(p.index) for p in hull
        )

    def update_hulls(self, *instances):
        txt = []
        for i, melkman in enumerate(instances):
            if melkman is None: continue
            txt.append(f"h{i + 1}: {self.hull_str(melkman.hull)}")
        self.hull_label["text"] = "\n".join(txt)

    def update(self):
        self.update_hulls(
            self.controller.melkman,
            self.controller.m1,
            self.controller.m2,
        )
        self.update_state()

class Canvas(tk.Canvas):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Canvas.__init__(self, parent,
            width  = 800,
            height = 600,
        )
        self["background"] = "white"

    def draw_circle(self, center, radius, fill, activefill, outline):
        return self.create_oval(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill          = fill,
            activefill    = activefill,
            outline       = outline,
            activeoutline = activefill,
        )

    # Bind events to multiple items.
    # * Right click: remove the point associated with the items.
    def bind_item(self, p, *ids):
        for id in ids:
            self.tag_bind(id, "<Button-3>",
                lambda *args: self.controller.delete(p)
            )

    def draw_nodes(self, collection):
        latestp = self.controller.latestp
        for p in collection:
            id1 = self.draw_circle(
                center     = p,
                radius     = 10 if p != latestp else 12,
                fill       = "white",
                activefill = "light slate blue",
                outline    = "firebrick2" if p != latestp else "dark slate blue",
            )
            id2 = self.create_text(
                p.x, p.y,
                text       = str(p.index),
                fill       = "gray15",
                activefill = "light slate blue"
            )
            self.bind_item(p, id1, id2)

    def draw_dots(self, collection):
        latestp = self.controller.latestp
        for p in collection:
            id = self.draw_circle(
                center     = p,
                radius     = 3 if p != latestp else 5,
                fill       = "gray15" if p != latestp else "dark slate blue",
                activefill = "light slate blue",
                outline    = "gray15" if p != latestp else "dark slate blue",
            )
            self.bind_item(p, id)

    def draw_edges(self, collection, color, width = 1, dash = None):
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

    def draw(self, melkman):
        self.draw_edges(melkman.lst, "gray15", dash = (5, 5))
        self.draw_dots(melkman.lst)
        self.draw_edges(melkman.hull, "red", width = 2)
        self.draw_nodes(melkman.hull)

    def update(self):
        self.delete("all")

        for melkman in (
            self.controller.melkman,
            self.controller.m1,
            self.controller.m2,
        ):
            if melkman is not None: self.draw(melkman)
