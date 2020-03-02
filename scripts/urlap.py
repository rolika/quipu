from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from szemely import Szemely
from telefon import Telefon
from email import Email
from cim import Cim


class SzemelyUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._elotag = StringVar()
        self._vezeteknev = StringVar()
        self._keresztnev = StringVar()
        self._nem = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="előtag").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._elotag, width=8).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._vezeteknev, width=32)
        self._fokusz.grid(row=1, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._keresztnev, width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="nem").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="nő", value="nő", variable=self._nem).grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self._nem).grid(row=3, column=2, sticky=W, padx=2, pady=2)
        self._nem.set("férfi")

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32)\
            .grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)

    @property
    def fokusz(self):
        return self._fokusz

    def beallit(self, szemely):
        self._elotag.set(szemely.elotag)
        self._vezeteknev.set(szemely.vezeteknev)
        self._keresztnev.set(szemely.keresztnev)
        self._nem.set(szemely.nem)
        self._megjegyzes.set(szemely.megjegyzes)

    def export(self):
        return Szemely(elotag=self._elotag.get(),
                      vezeteknev=self._vezeteknev.get(),
                      keresztnev=self._keresztnev.get(),
                      nem=self._nem.get(),
                      megjegyzes=self._megjegyzes.get())


class TelefonszamUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._telefonszam = StringVar()
        self._megjegyzes = StringVar()
        megjegyzes = ("alapértelmezett", "munkahelyi", "privát")
        self._megjegyzes.set(megjegyzes[0])

        Label(self, text="telefonszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._telefonszam, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megjegyzes, *megjegyzes).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, telefon):
        self._telefonszam.set(telefon.telefonszam)
        self._megjegyzes.set(telefon.megjegyzes)

    def export(self):
        return Telefon(telefonszam=self._telefonszam.get(), megjegyzes=self._megjegyzes.get())


class EmailcimUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._emailcim = StringVar()
        self._megjegyzes = StringVar()
        megjegyzes = ("alapértelmezett", "munkahelyi", "privát")
        self._megjegyzes.set(megjegyzes[0])

        Label(self, text="email-cím").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._emailcim, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megjegyzes, *megjegyzes).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, email):
        self._emailcim.set(email.emailcim)
        self._megjegyzes.set(email.megjegyzes)

    def export(self):
        return Email(emailcim=self._emailcim.get(), megjegyzes=self._megjegyzes.get())


class Valaszto(LabelFrame):
    def __init__(self, cimke, valasztek, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)
        self._valasztek = valasztek
        self._valaszto = Combobox(self, width=32)
        self.beallit(valasztek)
        self._valaszto.grid()

    def beallit(self, valasztek):
        self._valasztek = valasztek
        self._valaszto["values"] = [elem.listanezet() for elem in valasztek]
        try:
            self._valaszto.current(0)
        except TclError:
            self._valaszto.set("")

    @property
    def valaszto(self):
        return self._valaszto

    @property
    def elem(self):
        try:
            return self._valasztek[self._valaszto.current()]
        except IndexError:
            return None


class UjSzemelyUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új személy felvitele")

    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._szemelyurlap = SzemelyUrlap(self)
        self._szemelyurlap.pack(ipadx=2, ipady=2)
        return self._szemelyurlap.fokusz

    def validate(self):
        """Override Dialog.validate - adatok ellenőrzése"""
        szemely = self._szemelyurlap.export()
        if not szemely:
            messagebox.showwarning("Hiányos adat!", "Legalább az egyik nevet add meg!", parent=self)
            return False
        if szemely.meglevo(self._kon):
            messagebox.showwarning("A név már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True

    def apply(self):
        """Override Dialog.apply - helyes adatok feldolgozása"""
        szemely = self._szemelyurlap.export()
        if szemely.ment(self._kon):
            print("Bejegyzés mentve.")
        else:  # adatbázis-hiba visszajelzése
            print("Nem sikerült elmenteni.")


class SzemelyTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Személy törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)
        return self._nev_valaszto.valaszto

    def validate(self):
        szemely = self._nev_valaszto.elem
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN törlődik!", parent=self)
        return szemely and biztos

    def apply(self):
        szemely = self._nev_valaszto.elem
        self._kon.delete("telefon", szemely=szemely.azonosito)  # GDPR!
        self._kon.delete("email", szemely=szemely.azonosito)
        self._kon.delete("cim", szemely=szemely.azonosito)
        self._kon.delete("kontakt", szemely=szemely.azonosito)
        if szemely.torol(self._kon):
            print("Bejegyzés törölve.")
            self._nev_valaszto.beallit(self._nevsor())
        else:
            print("Nem sikerült törölni.")

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)


class SzemelyModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._szemely = None
        super().__init__(szulo, title="Személy módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._szemelyurlap = SzemelyUrlap(self)
        self._szemelyurlap.pack(ipadx=2, ipady=2)
        self._megjelenit(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._szemely = self._uj_szemely()
        if not self._szemely:
            messagebox.showwarning("Hiányos adat!", "Legalább az egyik nevet add meg!", parent=self)
            return False
        if self._szemely.meglevo(self._kon):
            messagebox.showwarning("A név már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True

    def apply(self):
        if self._szemely.ment(self._kon):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._nev_valaszto.beallit(self._nevsor())
        self._megjelenit(1)

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _megjelenit(self, event):
        self._szemelyurlap.beallit(self._nev_valaszto.elem or Szemely())

    def _uj_szemely(self):
        szemely = self._nev_valaszto.elem
        szemely.adatok = self._szemelyurlap.export()
        return szemely


class UjTelefonUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._telefonszam = None
        super().__init__(szulo, title="Új telefonszám hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self)
        self._telefonszam_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._telefonszam = self._telefonszam_urlap.export()
        if not self._telefonszam:
            messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
            return False
        return True

    def apply(self):
        self._telefonszam.szemely = self._nev_valaszto.elem.azonosito
        if self._telefonszam.ment(self._kon):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)


class TelefonTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._telefonszam = None
        super().__init__(szulo, title="Telefonszám törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("törlendő telefonszám", self._telefonszamok(), self)
        self._telefon_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._telefonszam = self._telefon_valaszto.elem
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return self._telefonszam and biztos

    def apply(self):
        if self._telefonszam.torol(self._kon):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.elem
        return [Telefon(**telefon) for telefon in self._kon.select("telefon", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())


class TelefonModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._telefonszam = None
        super().__init__(szulo, title="Telefonszám módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("módosítandó telefonszam", self._telefonszamok(), self)
        self._telefon_valaszto.valaszto.bind("<<ComboboxSelected>>", self._kiir_elerhetoseg)
        self._telefon_valaszto.pack(ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self)
        self._telefonszam_urlap.pack(ipadx=2, ipady=2)
        self._kiir_elerhetoseg(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._telefonszam = self._uj_telefonszam()
        if not self._telefonszam:
            messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
            return False
        return True

    def apply(self):
        if self._telefonszam.ment(self._kon):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.elem
        return [Telefon(**telefon) for telefon in self._kon.select("telefon", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())
        self._kiir_elerhetoseg(1)

    def _kiir_elerhetoseg(self, event):
        self._telefonszam_urlap.beallit(self._telefon_valaszto.elem or Telefon())

    def _uj_telefonszam(self):
        telefon = self._telefon_valaszto.elem
        if telefon:
            telefon.adatok = self._telefonszam_urlap.export()
        return telefon


class UjEmailUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._emailcim = None
        super().__init__(szulo, title="Új email-cím hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self)
        self._emailcim_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._emailcim = self._emailcim_urlap.export()
        if not self._emailcim:
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            return False
        return True

    def apply(self):
        self._emailcim.szemely = self._nev_valaszto.elem.azonosito
        if self._emailcim.ment(self._kon):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)


class EmailTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._emailcim = None
        super().__init__(szulo, title="Email-cím törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("törlendő email-cím", self._emailcimek(), self)
        self._email_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._emailcim = self._email_valaszto.elem
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return self._emailcim and biztos

    def apply(self):
        if self._emailcim.torol(self._kon):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _emailcimek(self):
        szemely = self._nev_valaszto.elem
        return [Email(**email) for email in self._kon.select("email", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())


class EmailModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._emailcim = None
        super().__init__(szulo, title="Email-cím módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("módosítandó email-cím", self._emailcimek(), self)
        self._email_valaszto.valaszto.bind("<<ComboboxSelected>>", self._kiir_elerhetoseg)
        self._email_valaszto.pack(ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self)
        self._emailcim_urlap.pack(ipadx=2, ipady=2)
        self._kiir_elerhetoseg(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._emailcim = self._uj_emailcim()
        if not self._emailcim:
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            return False
        return True

    def apply(self):
        if self._emailcim.ment(self._kon):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _emailcimek(self):
        szemely = self._nev_valaszto.elem
        return [Email(**email) for email in self._kon.select("email", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())
        self._kiir_elerhetoseg(1)

    def _kiir_elerhetoseg(self, event):
        self._emailcim_urlap.beallit(self._email_valaszto.elem or Email())

    def _uj_emailcim(self):
        email = self._email_valaszto.elem
        if email:
            email.adatok = self._emailcim_urlap.export()
        return email


if __name__ == "__main__":
    szulo = Tk()
    urlap = UjSzemelyUrlap(szulo)
    szulo.mainloop()

