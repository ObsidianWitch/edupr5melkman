import ui
from utils import Table
from melkman import Melkman
from spc import SimplePolygonalChain as SPC

class Mode:
    def __init__(self, window):
        self.window  = window
        self.melkman = None

    @classmethod
    def name(cls): return cls.__name__

    @property
    def latestp(self): return self.melkman.iter.current

    @property
    def area(self): return Table(
        x = 0, y = 0,
        width  =  self.window.canvas.winfo_width(),
        height =  self.window.canvas.winfo_height(),
    )

    def __len__(self):
        if self.melkman is None: return 0
        else: return len(self.melkman.spc)

class Interactive(Mode):
    def __init__(self, window):
        Mode.__init__(self, window)
        self.melkman = Melkman([])

    @property
    def finished(self): return False

    def next(self, p):
        self.melkman.add(p)
        self.window.update()

    def delete(self, i): pass

class Step(Mode):
    NPOINTS = 100

    def __init__(self, window):
        Mode.__init__(self, window)
        spc = SPC.generate(self.area, self.NPOINTS)
        self.melkman = Melkman(spc)
        self.m1 = Melkman(spc)
        self.m2 = Melkman([])

    @property
    def latestp(self): return self.m1.iter.current

    @property
    def finished(self): return self.m1.iter.finished

    def next(self, *args):
        self.m1.next()
        self.window.update()

    def delete_first(self):
        if not self.m2.hull:
            if not self.m1.hull: return
            self.m1, self.m2 = self.m1.split()
        self.m2.rewind()

    def delete_last(self): self.m1.rewind()

    def delete(self, i):
        if   i ==  0: self.delete_first()
        elif i == -1: self.delete_last()

        self.window.update()

class Test(Mode):
    NPOINTS = 300
    CHECKS  = 5000
    SLICES  = 10

    def __init__(self, window):
        Mode.__init__(self, window)
        self.passed  = 0
        self.failed  = 0
        self.cancel  = False

    @property
    def checks(self): return self.passed + self.failed

    @property
    def slice(self): return (self.checks % self.SLICES == 0)

    @property
    def finished(self): return self.checks >= self.CHECKS

    def next(self, *args):
        while not self.finished and not self.cancel:
            self.melkman = Melkman(SPC.generate(
                self.area, self.NPOINTS
            ))
            self.melkman.run()
            if self.melkman.check():
                self.passed += 1
                if self.slice: self.window.update()
            else: self.failed += 1 ; return False

    def delete(self, i): pass

# Controller allowing to switch between modes to manipulate the melkman
# algorithm.
# * Interactive: points are added individually to the simple polygonal chain.
# * Step: a simple polygonal chain is generated.
# * Test: algorithm robustness test.
class Controller:
    MODES = Table(
        interactive = Interactive,
        step        = Step,
        test        = Test,
    )

    def __init__(self):
        self.window = ui.Window(self)
        self.mode = Interactive(self.window)
        self.window.update()
        self.window.protocol('WM_DELETE_WINDOW', self.exit)

    # Expose mode and model attributes.
    def __getattr__(self, key): return getattr(self.mode, key, None)

    def select(self, mode):
        self.mode.cancel = True
        self.mode = mode(self.window)
        self.window.update()

    def delete(self, p = None, i = None):
        assert (i is not None) or (p is not None)
        if i is None: i = p.index
        self.mode.delete(i)

    def loop(self):
        self.window.mainloop()

    def exit(self):
        self.mode.cancel = True
        self.window.destroy()
