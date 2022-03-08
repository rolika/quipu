from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from datetime import date
from urlap import CimUrlap, Valaszto
from projekt import Projekt
from munkaresz import Munkaresz
from cim import Cim
from jelleg import Jelleg
from konstans import JELLEG, MUNKARESZ


class ProjektUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._projektszam = StringVar()
        self._megnevezes = StringVar()
        self._rovidnev = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="projektszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._projektszam, width=8, state=DISABLED)\
            .grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megnevezés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._megnevezes, width=32)
        self._fokusz.grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="rövid név").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._rovidnev, width=32).grid(row=2, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=3, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, projekt):
        self._projektszam.set("{}/{}".format(projekt.ev, projekt.szam))
        self._megnevezes.set(projekt.megnevezes)
        self._rovidnev.set(projekt.rovidnev)
        self._megjegyzes.set(projekt.megjegyzes)

    def export(self):
        return Projekt(
            megnevezes=self._megnevezes.get(),
            rovidnev=self._rovidnev.get(),
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
    def __init__(self, szulo, kon):
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

        if projekt.meglevo(self._kon.projekt)\
            and cim.meglevo(self._kon.projekt)\
                and munkaresz.meglevo(self._kon.projekt)\
                    and jelleg.meglevo(self._kon.projekt):
            messagebox.showwarning("Létező projekt!", "Pontosítsd!",
                                   parent=self)
            return False

        return True

    def apply(self):

        projekt = self._projekt_urlap.export()
        projekt.ev = self._ev
        projekt.szam = self._szam
        projekt.gyakorisag = 0

        if not (projekt_azonosito := projekt.ment(self._kon.projekt)):
            print("Nem sikerült elmenteni!")
            return

        munkaresz = self._munkaresz_urlap.export()
        munkaresz.projekt = projekt_azonosito
        if not (munkaresz_azonosito := munkaresz.ment(self._kon.projekt)):
            print("A munkarészt nem sikerült elmenteni!")
            return

        cim = self._cim_urlap.export()
        cim.munkaresz = munkaresz_azonosito
        jelleg = self._jelleg_urlap.export()
        jelleg.munkaresz = munkaresz_azonosito
        if not (cim.ment(self._kon.projekt) and jelleg.ment(self._kon.projekt)):
            print("A címet/jelleget nem sikerült elmenteni!")
            return

        print("Bejegyzés mentve.")

    def _kovetkezo_projektszam(self):
        utolso = self._kon.projekt.select("projekt", "szam", ev=self._ev, orderby="szam", ordering="DESC").fetchone()
        return utolso["szam"] + 1 if utolso else 1


class ProjektTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Projekt törlése")

    def body(self, szulo):
        self._projekt_valaszto = Valaszto("projekt", self._projektek(), self)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)
        return self._projekt_valaszto.valaszto

    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)

    def apply(self):
        hiba = False
        projekt = self._projekt_valaszto.elem
        for munkaresz in map(lambda mr: Munkaresz(**mr), self._kon.projekt.select("munkaresz", projekt=projekt.azonosito)):
            for cim in map(lambda cm: Cim(**cm), self._kon.projekt.select("cim", munkaresz=munkaresz.azonosito)):
                if not cim.torol(self._kon.projekt):
                    hiba = True
            for jelleg in map(lambda jg: Jelleg(**jg), self._kon.projekt.select("jelleg", munkaresz=munkaresz.azonosito)):
                if not jelleg.torol(self._kon.projekt):
                    hiba = True
            if not munkaresz.torol(self._kon.projekt):
                hiba = True
        if not projekt.torol(self._kon.projekt):
            hiba = True
        if hiba:
            print("Nem sikerült törölni.")
        else:
            print("{}: Bejegyzés törölve.".format(projekt))
            self._projekt_valaszto.beallit(self._projektek())

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._kon.projekt.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))


class ProjektModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Projekt módosítása")

    def body(self, szulo):
        self._projekt_valaszto = Valaszto("megnevezés", self._projektek(), self)
        self._projekt_valaszto.set_callback(self._projekt_megjelenit)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)

        megnevezes = LabelFrame(self, text="projekt neve")
        self._projekt_urlap = ProjektUrlap(megnevezes)
        self._projekt_urlap.pack(ipadx=2, ipady=2)
        self._projekt_megjelenit(1)
        megnevezes.pack(fill=X, padx=2, pady=2)

        return self._projekt_valaszto.valaszto

    def validate(self):
        """Ezen a ponton a projektek a projektszám miatt mindenképpen különbözni fognak egymástól."""
        return True

    def apply(self):
        projekt = self._modositott_projekt()
        if projekt.ment(self._kon.projekt):
            print("{}: Bejegyzés módosítva.".format(projekt))
        else:
            print("Nem sikerült módosítani.")
        self._projekt_valaszto.beallit(self._projektek())
        self._projekt_megjelenit(1)

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._kon.projekt.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _projekt_megjelenit(self, event):
        self._projekt_urlap.beallit(self._projekt_valaszto.elem or Projekt())

    def _modositott_projekt(self):
        projekt = self._projekt_valaszto.elem
        projekt.adatok = self._projekt_urlap.export()
        return projekt


class UjMunkareszUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új munkarész felvitele")

    def body(self, szulo):
        self._projekt_valaszto = Valaszto("projekt", self._projektek(), self)
        self._projekt_valaszto.set_callback(self._cim_megjelenit)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)

        munkaresz = LabelFrame(self, text="munkarész")
        self._munkaresz_urlap = MunkareszUrlap(munkaresz)
        self._munkaresz_urlap.pack(ipadx=2, ipady=2)
        munkaresz.pack(fill=X, padx=2, pady=2)

        cim = LabelFrame(self, text="munkarész címe")
        self._cim_urlap = CimUrlap(cim)
        self._cim_urlap.pack(ipadx=2, ipady=2)
        self._cim_megjelenit(1)
        cim.pack(padx=2, pady=2)

        jelleg = LabelFrame(self, text="munkarész jellege")
        self._jelleg_urlap = JellegUrlap(jelleg)
        self._jelleg_urlap.pack(ipadx=2, ipady=2)
        jelleg.pack(fill=X, padx=2, pady=2)

        return self._projekt_valaszto.valaszto

    def validate(self):
        munkaresz = self._munkaresz_urlap.export()
        cim = self._cim_urlap.export()
        jelleg = self._jelleg_urlap.export()

        if not munkaresz:
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet add meg!", parent=self)
            return False

        if munkaresz.meglevo(self._kon.projekt) and cim.meglevo(self._kon.projekt) and jelleg.meglevo(self._kon.projekt):
            messagebox.showwarning("Létező munkarész!", "Pontosítsd!", parent=self)
            return False

        return True

    def apply(self):
        projekt = self._projekt_valaszto.elem
        munkaresz = self._munkaresz_urlap.export()
        munkaresz.projekt = projekt.azonosito

        munkaresz = self._munkaresz_urlap.export()
        munkaresz.projekt = projekt.azonosito
        if not (munkaresz_azonosito := munkaresz.ment(self._kon.projekt)):
            print("A munkarészt nem sikerült elmenteni!")
            return

        cim = self._cim_urlap.export()
        cim.munkaresz = munkaresz_azonosito
        jelleg = self._jelleg_urlap.export()
        jelleg.munkaresz = munkaresz_azonosito
        if not (cim.ment(self._kon.projekt) and jelleg.ment(self._kon.projekt)):
            print("A címet/jelleget nem sikerült elmenteni!")
            return

        print("Bejegyzés mentve.")

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._kon.projekt.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _cim_megjelenit(self, event):
        projekt = self._projekt_valaszto.elem
        if (munkaresz := self._kon.projekt.select("munkaresz", projekt=projekt.azonosito).fetchone())\
            and (cim := self._kon.projekt.select("cim", munkaresz=Munkaresz(**munkaresz).azonosito).fetchone()):
            self._cim_urlap.beallit(Cim(**cim))
        else:
            self._cim_urlap.beallit(Cim())


class MunkareszTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Munkarész törlése")

    def body(self, szulo):
        self._munkaresz_valaszto = Valaszto("munkarész", self._munkareszek(), self)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)
        return self._munkaresz_valaszto.valaszto

    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)

    def apply(self):
        hiba = False
        jelleg = self._munkaresz_valaszto.elem
        munkaresz = self._kon.projekt.select("munkaresz", azonosito=jelleg.munkaresz).fetchone()
        munkaresz = Munkaresz(**munkaresz)
        cim = self._kon.projekt.select("cim", munkaresz=munkaresz.azonosito).fetchone()
        cim = Cim(**cim)
        if not cim.torol(self._kon.projekt):
            hiba = True
        if not jelleg.torol(self._kon.projekt):
            hiba = True
        if not self._kon.projekt.select("jelleg", munkaresz=jelleg.munkaresz).fetchone():
            if not munkaresz.torol(self._kon.projekt):
                hiba = True
        if hiba:
            print("Nem sikerült törölni.")
        else:
            print("Bejegyzés törölve.")

    def _munkareszek(self):
        return sorted(map(lambda jelleg: Jelleg(kon=self._kon, **jelleg),
                          self._kon.projekt.select("jelleg")), key=repr)


class MunkareszModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Munkarész módosítása")

    def body(self, szulo):
        self._munkaresz_valaszto = Valaszto("munkarész", self._munkareszek(), self)
        self._munkaresz_valaszto.set_callback(self._munkaresz_megjelenit)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)

        munkaresz = LabelFrame(self, text="munkarész")
        self._munkaresz_urlap = MunkareszUrlap(munkaresz)
        self._munkaresz_urlap.pack(ipadx=2, ipady=2)
        munkaresz.pack(fill=X, padx=2, pady=2)

        cim = LabelFrame(self, text="munkarész címe")
        self._cim_urlap = CimUrlap(cim)
        self._cim_urlap.pack(ipadx=2, ipady=2)
        cim.pack(padx=2, pady=2)

        jelleg = LabelFrame(self, text="munkarész jellege")
        self._jelleg_urlap = JellegUrlap(jelleg)
        self._jelleg_urlap.pack(ipadx=2, ipady=2)
        jelleg.pack(fill=X, padx=2, pady=2)

        self._munkaresz_megjelenit(1)
        return self._munkaresz_valaszto.valaszto

    def validate(self):
        munkaresz = self._munkaresz_urlap.export()
        cim = self._cim_urlap.export()
        jelleg = self._jelleg_urlap.export()

        if not munkaresz:
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet add meg!", parent=self)
            return False

        if munkaresz.meglevo(self._kon.projekt) and cim.meglevo(self._kon.projekt) and jelleg.meglevo(self._kon.projekt):
            messagebox.showwarning("Létező munkarész!", "Pontosítsd!", parent=self)
            return False

        return True

    def apply(self):
        munkaresz, cim, jelleg = self._modositott_munkaresz()
        if munkaresz.ment(self._kon.projekt) and cim.ment(self._kon.projekt) and jelleg.ment(self._kon.projekt):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni!")
    
    def _munkareszek(self):
        return sorted(map(lambda jelleg: Jelleg(kon=self._kon, **jelleg),
                          self._kon.projekt.select("jelleg")), key=repr)
    
    def _munkaresz_kivalaszt(self, event):
        self._munkaresz_valaszto.beallit(self._munkareszek())
        self._munkaresz_megjelenit(1)

    def _munkaresz_megjelenit(self, event):
        munkaresz, cim, jelleg = self._meglevo_munkaresz()
        self._munkaresz_urlap.beallit(munkaresz)
        self._cim_urlap.beallit(cim)
        self._jelleg_urlap.beallit(jelleg)
    
    def _meglevo_munkaresz(self):
        jelleg = self._munkaresz_valaszto.elem
        munkaresz = self._kon.projekt.select("munkaresz", azonosito=jelleg.munkaresz).fetchone()
        munkaresz = Munkaresz(**munkaresz)
        cim = self._kon.projekt.select("cim", munkaresz=munkaresz.azonosito).fetchone()
        cim = Cim(**cim)
        return (munkaresz, cim, jelleg)
    
    def _modositott_munkaresz(self):        
        munkaresz, cim, jelleg = self._meglevo_munkaresz()
        munkaresz.adatok = self._munkaresz_urlap.export()
        cim.adatok = self._cim_urlap.export()
        jelleg.adatok = self._jelleg_urlap.export()
        return (munkaresz, cim, jelleg)


if __name__== "__main__":
    UjProjektUrlap(Tk())