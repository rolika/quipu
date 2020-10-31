from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, Labelframe
from urlap import CimUrlap
from cim import Cim
from konstans import JELLEG, MUNKARESZ


class UjProjektUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        # super() előtt kell legyenek
        self._kon = kon 
        self._megnevezes = StringVar()
        self._munkaresz = StringVar()
        self._jelleg = StringVar()
        self._megjegyzes = StringVar()

        super().__init__(szulo, title="Új projekt felvitele")
    
    def body(self, szulo):

        megnevezes = LabelFrame(self, text="projekt neve")
        nev = Entry(megnevezes, textvariable=self._megnevezes)
        nev.pack(fill=X, padx=2, pady=2)
        megnevezes.pack(fill=X, padx=2, pady=2)

        cim = LabelFrame(self, text="projekt címe")
        self._cim_urlap = CimUrlap(cim)
        self._cim_urlap.pack(ipadx=2, ipady=2)
        cim.pack(padx=2, pady=2)

        munkaresz = LabelFrame(self, text="munkarész")
        self._munkaresz.set(MUNKARESZ[0])
        Combobox(munkaresz, textvariable=self._munkaresz, values=MUNKARESZ).pack(fill=X, padx=2, pady=2)
        munkaresz.pack(fill=X, padx=2, pady=2)

        jelleg = LabelFrame(self, text="jelleg")
        self._jelleg.set(JELLEG[0])
        OptionMenu(jelleg, self._jelleg, *JELLEG).pack(fill=X, ipadx=2, ipady=2)
        jelleg.pack(fill=X, padx=2, pady=2)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes).pack(fill=X, padx=2, pady=2)
        megjegyzes.pack(fill=X, padx=2, pady=2)

        nev.focus_set()
    
    def validate(self):
        pass

    def apply(self):
        pass


class ProjektTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Projekt törlése")


class ProjektModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Projekt módosítása")


class UjMunkareszUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új munkarész felvitele")


class MunkareszTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Munkarész törlése")


class MunkareszModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Munkarész módosítása")


class UjMunkareszCimUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új cím felvitele")


class MunkareszCimTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Cím törlése")


class MunkareszCimModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Cím módosítása")


if __name__== "__main__":
    UjProjektUrlap(Tk())