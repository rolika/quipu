from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from urlap import CimUrlap
from projekt import Projekt
from munkaresz import Munkaresz
from jelleg import Jelleg
from konstans import JELLEG, MUNKARESZ


class ProjektUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._megnevezes = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="megnevezés").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megnevezes, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, projekt):
        self._megnevezes.set(projekt.megnevezes)
        self._megjegyzes.set(projekt.megjegyzes)

    def export(self):
        return Projekt(
            megnevezes=self._megnevezes.get(),
            megjegyzes=self._megjegyzes.get()
        )


class MunkareszUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._megnevezes = StringVar()
        self._enaplo = IntVar()
        self._megjegyzes = StringVar()

        Label(self, text="megnevezés").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Combobox(self, textvariable=self._megnevezes, values=MUNKARESZ).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="e-napló").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Checkbutton(self, variable=self._enaplo).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=2, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, munkaresz):
        self._megnevezes.set(munkaresz.megnevezes)
        self._enaplo.set(munkaresz.enaplo)
        self._megjegyzes.set(munkaresz.megjegyzes)

    def export(self):
        return Munkaresz(
            megnevezes=self._megnevezes.get(),
            enaplo=self._enaplo.get(),
            megjegyzes=self._megjegyzes.get()
        )


class JellegUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._megnevezes = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="megnevezés").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megnevezes, *JELLEG).grid(row=0, column=1, sticky=EW, padx=2, pady=2)
        self._megnevezes.set(JELLEG[0])

        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, jelleg):
        self._megnevezes.set(jelleg.megnevezes)
        self._megjegyzes.set(jelleg.megjegyzes)

    def export(self):
        return Jelleg(
            megnevezes=self._megnevezes.get(),
            megjegyzes=self._megjegyzes.get()
        )


class UjProjektUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        # super() előtt kell legyenek
        self._kon = kon

        super().__init__(szulo, title="Új projekt felvitele")

    def body(self, szulo):

        megnevezes = LabelFrame(self, text="projekt neve")
        self._projekt_urlap = ProjektUrlap(megnevezes)
        self._projekt_urlap.pack(ipadx=2, ipady=2)
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

        megnevezes.focus_set()

    def validate(self):
        projekt = self._projekt_urlap.export()
        cim = self._cim_urlap.export()
        munkaresz = self._munkaresz_urlap.export()
        jelleg = self._jelleg_urlap.export()

        if not (projekt and cim and munkaresz):
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet, a helységet és a munkarészt add meg!",
                                   parent=self)
            return False

        if projekt.meglevo(self._kon)\
            and cim.meglevo(self._kon)\
                and munkaresz.meglevo(self._kon)\
                    and jelleg.meglevo(self._kon):
            messagebox.showwarning("Létező projekt!", "Különböztesd meg megjegyzésben!",
                                   parent=self)
            return False
        
        return True

    def apply(self):

        projekt = self._projekt_urlap.export()
        if not (projekt_azonosito := projekt.ment(self._kon)):
            print("Nem sikerült elmenteni!")
            return

        munkaresz = self._munkaresz_urlap.export()
        munkaresz.projekt = projekt_azonosito
        if not (munkaresz_azonosito := munkaresz.ment(self._kon)):
            print("A munkarészt nem sikerült elmenteni!")
            return

        cim = self._cim_urlap.export()
        cim.munkaresz = munkaresz_azonosito
        jelleg = self._jelleg_urlap.export()
        jelleg.munkaresz = munkaresz_azonosito
        if not (cim.ment(self._kon) and jelleg.ment(self._kon)):
            print("A címet/jelleget nem sikerült elmenteni!")
            return

        print("Bejegyzés mentve.")


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