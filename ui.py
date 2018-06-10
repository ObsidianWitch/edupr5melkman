import tkinter as tk

class Window(tk.Tk):
    def __init__(self, melkman):
        self.melkman = melkman

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
        for i, mode in enumerate(self.melkman.MODES):
            add_mode = lambda mode: menu_button.menu.add_command(
                label   = mode.NAME,
                command = lambda: self.select_mode(mode),
            ) ; add_mode(mode)

        self.information = Information(top_frame, melkman)
        self.information.grid(row = 0, column = 1, sticky = tk.W)

        self.canvas = Canvas(self, melkman)
        self.canvas.grid(row = 1, column = 0)
        self.canvas.bind("<Button-1>", self.click)

    def select_mode(self, mode):
        self.melkman.select(mode)
        self.information.update()
        self.canvas.update()

    def click(self, event):
        def process():
            loop = self.melkman.next((event.x, event.y))
            self.information.update()
            self.canvas.update()
            tk.Tk.update(self)
            return loop
        while process(): pass

class Information(tk.Frame):
    def __init__(self, parent, melkman):
        self.melkman = melkman

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

        self.update()

    def update_state(self):
        txt = []
        txt.append(f"Mode: {self.melkman.NAME}")

        if self.melkman.instance is not None: txt.append(
            f"Points: {len(self.melkman.lst)}"
        )
        else: txt.append("Points: 0")

        if self.melkman.checks is not None: txt.append(
            f"Checks: ✓ {self.melkman.passed}"
            f" / X {self.melkman.failed}"
            f" / N {self.melkman.CHECKS}"
        )

        if self.melkman.finished: txt.append("finished")

        self.state_label["text"] = " | ".join(txt)

    def update_hull(self):
        txt = "hull: "
        if not self.melkman.hull: txt += "∅"
        else: txt += ", ".join((
            str(p.index) for p in self.melkman.hull
        ))
        self.hull_label["text"] = txt

    def update(self):
        self.update_state()
        self.update_hull()

class Canvas(tk.Canvas):
    def __init__(self, parent, melkman):
        self.melkman = melkman

        tk.Canvas.__init__(self, parent,
            width  = 800,
            height = 600,
        )
        self["background"] = "white"

    def draw_circle(self, center, radius, bg_color, bd_color):
        self.create_oval(
            center.x - radius, center.y - radius,
            center.x + radius, center.y + radius,
            fill    = bg_color,
            outline = bd_color,
        )

    def draw_nodes(self, collection):
        latestp = self.melkman.latestp
        for p in collection:
            self.draw_circle(
                center   = p,
                radius   = 10 if p != latestp else 12,
                bg_color = "white",
                bd_color = "red" if p != latestp else "magenta",
            )
            self.create_text(
                p.x, p.y,
                text = str(p.index),
            )

    def draw_dots(self, collection):
        latestp = self.melkman.latestp
        for p in collection:
            self.draw_circle(
                center   = p,
                radius   = 2 if p != latestp else 4,
                bg_color = "black" if p != latestp else "magenta",
                bd_color = "black" if p != latestp else "magenta",
            )

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
        if self.melkman.instance is None: return
        self.draw_edges(self.melkman.lst, "black")
        self.draw_dots(self.melkman.lst)
        self.draw_edges(self.melkman.hull, "red")
        self.draw_nodes(self.melkman.hull)
