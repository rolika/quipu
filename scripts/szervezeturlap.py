from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from urlap import TelefonszamUrlap, EmailcimUrlap, CimUrlap, Valaszto
from szervezet import Szervezet
from telefon import Telefon
from email import Email
from cim import Cim


class SzervezetUrlap(Frame):
    def __init__(self, szulo=None, **kw):
        super().__init__(master=szulo, **kw)

        self._rovidnev = StringVar()
        self._teljesnev = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="rövid név").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._rovidnev, width=32)
        self._fokusz.grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="teljes név").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._teljesnev, width=32).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=3, column=1, sticky=W, padx=2, pady=2)
    
    @property
    def fokusz(self):
        return self._fokusz
    
    def beallit(self, szervezet):
        self._rovidnev.set(szervezet.rovidnev)
        self._teljesnev.set(szervezet.teljesnev)
        self._megjegyzes.set(szervezet.megjegyzes)

    def export(self):
        return Szervezet(
            rovidnev=self._rovidnev.get(),
            teljesnev=self._teljesnev.get(),
            megjegyzes=self._megjegyzes.get()
        )


class UjSzervezetUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Új szervezet felvitele")
    
    def body(self, szulo):
        self._szervezeturlap = SzervezetUrlap(self)
        self._szervezeturlap.pack(ipadx=2, ipady=2)
        return self._szervezeturlap.fokusz

    def validate(self):
        szervezet = self._szervezeturlap.export()
        if not szervezet:
            messagebox.showwarning("Hiányos adat!", "Legalább a rövid nevet add meg!", parent=self)
            return False
        if szervezet.meglevo(self._kon):
            messagebox.showwarning("Hiba!", "Ez a szervezet már szerepel az adatbázisban.")
            return False
        return True
    
    def apply(self):
        szervezet = self._szervezeturlap.export()
        if szervezet.ment(self._kon):
            print("{}: Bejegyzés elmentve.".format(szervezet))
        else:
            print("Nem sikerült elmenteni.")


class SzervezetTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Szervezet törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)
        return self._nev_valaszto.valaszto

    def validate(self):
        szervezet = self._nev_valaszto.elem
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)
        return szervezet and biztos

    def apply(self):
        szervezet = self._nev_valaszto.elem
        self._kon.delete("telefon", szervezet=szervezet.azonosito)
        self._kon.delete("email", szervezet=szervezet.azonosito)
        self._kon.delete("cim", szervezet=szervezet.azonosito)
        self._kon.delete("kontakt", szervezet=szervezet.azonosito)
        if szervezet.torol(self._kon):
            print("{}: Bejegyzés törölve.".format(szervezet))
            self._nev_valaszto.beallit(self._nevsor())
        else:
            print("Nem sikerült törölni.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.select("szervezet")), key=repr)


class SzervezetModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Szervezet módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._szervezeturlap = SzervezetUrlap(self)
        self._szervezeturlap.pack(ipadx=2, ipady=2)
        self._megjelenit(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        szervezet = self._uj_szervezet()
        if not szervezet:
            messagebox.showwarning("Hiányos adat!", "Legalább a rövid nevet add meg!", parent=self)
            return False
        if szervezet.meglevo(self._kon):
            messagebox.showwarning("Hiba!", "Ez a szervezet már szerepel az adatbázisban.", parent=self)
            return False
        return True

    def apply(self):
        szervezet = self._uj_szervezet()
        if szervezet.ment(self._kon):
            print("{}: Bejegyzés módosítva.".format(szervezet))
        else:
            print("Nem sikerült módosítani.")
        self._nev_valaszto.beallit(self._nevsor())
        self._megjelenit(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.select("szervezet")), key=repr)

    def _megjelenit(self, event):
        self._szervezeturlap.beallit(self._nev_valaszto.elem or Szervezet())

    def _uj_szervezet(self):
        szervezet = self._nev_valaszto.elem
        szervezet.adatok = self._szervezeturlap.export()
        return szervezet


if __name__ == "__main__":
    sz = SzervezetUrlap()
    sz.pack()
    sz.mainloop()
