from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from datetime import date
from urlap import CimUrlap, Valaszto
from projekt import Projekt
from munkaresz import Munkaresz
from jelleg import Jelleg
from konstans import JELLEG, MUNKARESZ


class ProjektUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._projektszam = StringVar()
        self._megnevezes = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="projektszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._projektszam, width=8, state=DISABLED)\
            .grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megnevezés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._megnevezes, width=32)
        self._fokusz.grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=2, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, projekt):
        self._megnevezes.set(projekt.megnevezes)
        self._megjegyzes.set(projekt.megjegyzes)

    def export(self):
        return Projekt(
            megnevezes=self._megnevezes.get(),
            megjegyzes=self._megjegyzes.get()
        )
    
    @property
    def projektszam(self):
        return self._projektszam.get()
    
    @projektszam.setter
    def projektszam(self, szam):
        self._projektszam.set(szam)

    @property
    def fokusz(self):
        return self._fokusz


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
        self._ev = date.today().strftime("%y")
        self._szam = self._kovetkezo_projektszam()

        super().__init__(szulo, title="Új projekt felvitele")

    def body(self, szulo):

        megnevezes = LabelFrame(self, text="projekt neve")
        self._projekt_urlap = ProjektUrlap(megnevezes)
        self._projekt_urlap.pack(ipadx=2, ipady=2)
        self._projekt_urlap.projektszam = "{}/{}".format(self._ev, self._szam)
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

        return self._projekt_urlap.fokusz

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
        projekt.ev = self._ev
        projekt.szam = self._szam
        projekt.gyakorisag = 0

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
    
    def _kovetkezo_projektszam(self):
        utolso = self._kon.select("projekt", "szam", ev=self._ev, orderby="szam", ordering="DESC").fetchone()
        return utolso["szam"] + 1 if utolso["szam"] else 1

class ProjektTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Projekt törlése")

    def body(self, szulo):
        self._projekt_valaszto = Valaszto("megnevezés", self._nevsor(), self)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)
        return self._projekt_valaszto.valaszto
    
    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)
    
    def apply(self):
        projekt = self._projekt_valaszto.elem
        munkareszek = self._kon.select("munkaresz", "projekt", projekt=projekt.azonosito)
        self._kon.delete("munkaresz", projekt=projekt.azonosito)
        for munkaresz in munkareszek:
            self._kon.delete("cim", munkaresz=munkaresz["azonosito"])
            self._kon.delete("jelleg", munkaresz=munkaresz["azonosito"])
        if projekt.torol(self._kon):
            print("{}: Bejegyzés törölve.".format(projekt))
            self._projekt_valaszto.beallit(self._nevsor())
        else:
            print("Nem sikerült törölni.")
    
    def _nevsor(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._kon.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

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


class UjJellegUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új jelleg felvitele")


class JellegTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Jelleg törlése")


class JellegModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Jelleg módosítása")


if __name__== "__main__":
    UjProjektUrlap(Tk())