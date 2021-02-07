from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from urlap import CimUrlap, MunkareszUrlap, JellegUrlap
from projekt import Projekt
from konstans import JELLEG, MUNKARESZ


class UjProjektUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        # super() előtt kell legyenek
        self._kon = kon
        self._megnevezes = StringVar()
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
        self._munkaresz_urlap = MunkareszUrlap(munkaresz)
        self._munkaresz_urlap.pack(ipadx=2, ipady=2)
        munkaresz.pack(fill=X, padx=2, pady=2)

        jelleg = LabelFrame(self, text="jelleg")
        self._jelleg_urlap = JellegUrlap(jelleg)
        self._jelleg_urlap.pack(ipadx=2, ipady=2)
        jelleg.pack(fill=X, padx=2, pady=2)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes).pack(fill=X, padx=2, pady=2)
        megjegyzes.pack(fill=X, padx=2, pady=2)

        nev.focus_set()

    def validate(self):
        if not self.export():
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet, a helységet és a munkarészt add meg!",
                                   parent=self)
            return False
        return True

    def apply(self):
        pass

    def export(self):
        return Projekt(
            megnevezes=self._megnevezes.get(),
            cim=self._cim_urlap.export(),
            munkaresz=self._munkaresz_urlap.export(),
            jelleg=self._jelleg_urlap.export(),
            megjegyzes=self._megjegyzes.get()
        )


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