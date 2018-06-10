import tkinter as tk

class Window(tk.Tk):
    def __init__(self, controller):
        self.controller = controller

        tk.Tk.__init__(self)
        self.title("Melkman")
        self.resizable(False, False)

        top_frame = tk.Frame(self)
        top_frame.grid(row = 0, column = 0, sticky = tk.W)

        menu_button = tk.Menubutton(top_frame,
            text   = "New",
            relief = tk.RAISED
        )
        menu_button.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.E + tk.W)
        menu_button.menu = tk.Menu(menu_button)
        menu_button["menu"] = menu_button.menu
        for i, mode in enumerate(self.controller.MODES):
            add_mode = lambda mode: menu_button.menu.add_command(
                label   = mode.NAME,
                command = lambda: self.select_mode(mode),
            ) ; add_mode(mode)

        self.information = Information(top_frame, controller)
        self.information.grid(row = 0, column = 1, sticky = tk.W)

        self.canvas = Canvas(self, controller)
        self.canvas.grid(row = 1, column = 0)
        self.canvas.bind("<Button-1>", self.add_click)

    def select_mode(self, mode):
        self.controller.select(mode)
        self.update()

    def add_click(self, event):
        self.controller.next((event.x, event.y))

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

        if self.controller.melkman is not None: txt.append(
            f"Points: {len(self.controller.lst)}"
        )
        else: txt.append("Points: 0")

        if self.controller.checks is not None: txt.append(
            f"Checks: ✓ {self.controller.passed}"
            f" / X {self.controller.failed}"
            f" / N {self.controller.CHECKS}"
        )

        if self.controller.finished: txt.append("finished")

        self.state_label["text"] = " | ".join(txt)

    def update_hull(self):
        txt = "hull: "
        if not self.controller.hull: txt += "∅"
        else: txt += ", ".join((
            str(p.index) for p in self.controller.hull
        ))
        self.hull_label["text"] = txt

    def update(self):
        self.update_state()
        self.update_hull()

class Canvas(tk.Canvas):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Canvas.__init__(self, parent,
            width  = 800,
            height = 600,
        )
        self["background"] = "white"

    def draw_circle(self, center, radius, bg_color, bd_color):
        return self.create_oval(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill    = bg_color,
            outline = bd_color,
        )

    def resize_circle(self, tag, px):
        x0, y0, x1, y1 = self.coords(tag)
        self.coords(tag,
            x0 - px, y0 - px,
            x1 + px, y1 + px,
        )

    # Bind events to a circle and its associated items. The circle's tag is
    # `tags[0]`. `tags[1:]` are the other items we want to bind to the same
    # events as the circle.
    # * Enter: increase the size of the circle
    # * Leave: decrease the size of the circle
    # * Right click: remove point associated with the circle
    def bind_circle(self, p, *tags):
        pass
        circle_tag = tags[0]
        for tag in tags:
            self.tag_bind(tag, "<Enter>",
                lambda *args: self.resize_circle(circle_tag,  2)
            )
            self.tag_bind(tag, "<Leave>",
                lambda *args: self.resize_circle(circle_tag, -2)
            )
            self.tag_bind(tag, "<Button-3>",
                lambda *args: self.controller.delete(p)
            )

    def draw_nodes(self, collection):
        latestp = self.controller.latestp
        for p in collection:
            tag1 = self.draw_circle(
                center   = p,
                radius   = 10 if p != latestp else 12,
                bg_color = "white",
                bd_color = "red" if p != latestp else "magenta",
            )
            tag2 = self.create_text(
                p.x, p.y,
                text = str(p.index),
            )
            self.bind_circle(p, tag1, tag2)

    def draw_dots(self, collection):
        latestp = self.controller.latestp
        for p in collection:
            tag = self.draw_circle(
                center   = p,
                radius   = 2 if p != latestp else 4,
                bg_color = "black" if p != latestp else "magenta",
                bd_color = "black" if p != latestp else "magenta",
            )
            self.bind_circle(p, tag)

    def draw_edges(self, collection, color):
        for i, _ in enumerate(collection):
            if i == len(collection) - 1: return
            p1 = collection[i]
            p2 = collection[i + 1]
            self.create_line(
                p1.x, p1.y,
                p2.x, p2.y,
                fill = color,
            )

    def update(self):
        self.delete("all")
        if self.controller.melkman is None: return
        self.draw_edges(self.controller.lst, "black")
        self.draw_dots(self.controller.lst)
        self.draw_edges(self.controller.hull, "red")
        self.draw_nodes(self.controller.hull)
