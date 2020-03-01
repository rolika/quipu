from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from szemely import Szemely
from telefon import Telefon
from email import Email


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


class TelefonszamUrlap(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="telefonszám", **kw)

        self.telefonszam = StringVar()
        self.megjegyzes = StringVar()
        megjegyzes = ("alapértelmezett", "munkahelyi", "privát")
        self.megjegyzes.set(megjegyzes[0])

        Label(self, text="telefonszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.telefonszam, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self.megjegyzes, *megjegyzes).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self.grid()

    def beallit(self, telefon):
        self.telefonszam.set(telefon.telefonszam)
        self.megjegyzes.set(telefon.megjegyzes)

    def export(self):
        return Telefon(telefonszam=self.telefonszam.get(), megjegyzes=self.megjegyzes.get())


class EmailcimUrlap(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="email-cím", **kw)

        self.emailcim = StringVar()
        self.megjegyzes = StringVar()
        megjegyzes = ("alapértelmezett", "munkahelyi", "privát")
        self.megjegyzes.set(megjegyzes[0])

        Label(self, text="email-cím").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.emailcim, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self.megjegyzes, *megjegyzes).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self.grid()

    def beallit(self, email):
        self.emailcim.set(email.emailcim)
        self.megjegyzes.set(email.megjegyzes)

    def export(self):
        return Email(emailcim=self.emailcim.get(), megjegyzes=self.megjegyzes.get())


class Valaszto(LabelFrame):
    def __init__(self, cimke, valasztek, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)
        self.valasztek = valasztek
        self.valaszto = Combobox(self, width=32)
        self.beallit(valasztek)
        self.valaszto.grid()

    def beallit(self, valasztek):
        self.valasztek = valasztek
        self.valaszto["values"] = [elem.listanezet() for elem in valasztek]
        try:
            self.valaszto.current(0)
        except TclError:
            self.valaszto.set("")

    def azonosito(self):
        try:
            return self.valasztek[self.valaszto.current()].azonosito
        except IndexError:
            return None

    @property
    def idx(self):
        return self.valaszto.current()


class KezeloGomb(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.master = master
        self.valasz = False

        self.megse = Button(self, text="mégse", command=self.winfo_toplevel().destroy, width=8)
        self.ok = Button(self, text="OK", command=self.rendben, width=8)

        self.megse.grid(row=0, column=0, padx=2, pady=2)
        self.ok.grid(row=0, column=1, padx=2, pady=2)

    def rendben(self):
        self.valasz = True
        self.winfo_toplevel().destroy()


class UjSzemelyUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Új személy felvitele")
    
    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._szemelyurlap = SzemelyUrlap(self)
        self._szemelyurlap.pack()
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


class SzemelyTorloUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)

        self._kon = kon

        self._nev_valaszto = Valaszto("személy törlése", self._nevsor(), self)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "törlés"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._torol
        kezelo.grid(row=1, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _torol(self):
        idx = self._nev_valaszto.idx
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN törlődik!", parent=self)
        if idx >= 0 and biztos:
            szemely = self._nevsor()[idx]
            self._kon.delete("telefon", szemely=szemely.azonosito)  # GDPR!
            self._kon.delete("email", szemely=szemely.azonosito)
            self._kon.delete("cim", szemely=szemely.azonosito)
            self._kon.delete("kontakt", szemely=szemely.azonosito)
            if szemely.torol(self._kon):
                print("Bejegyzés törölve.")
                self._nev_valaszto.beallit(self._nevsor())
            else:
                print("Nem sikerült törölni.")


class SzemelyModositoUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)

        self._kon = kon

        self._nev_valaszto = Valaszto("Személy módosítása", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._szemelyurlap = SzemelyUrlap(self)
        self._szemelyurlap.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)
        self._megjelenit(1)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "módosít"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._modosit
        kezelo.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _megjelenit(self, event):
        idx = self._nev_valaszto.idx
        if idx >= 0:
            szemely = self._nevsor()[idx]
        else:
            szemely = Szemely()
        self._szemelyurlap.beallit(szemely)

    def _modosit(self):
        idx = self._nev_valaszto.idx
        if idx >= 0:
            szemely = self._nevsor()[idx]
            szemely.adatok = self._szemelyurlap.export()
            if szemely:
                if szemely.meglevo(self._kon):
                    messagebox.showwarning("A név már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
                    return
                if szemely.ment(self._kon):
                    print("Bejegyzés módosítva.")
                else:
                    print("Nem sikerült módosítani.")
                self._nev_valaszto.beallit(self._nevsor())
                self._megjelenit(1)
            else:
                messagebox.showwarning("Hiányos adat!", "Legalább az egyik nevet add meg!", parent=self)


class UjTelefonUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("telefon hozzáadása", self._nevsor(), self)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self)
        self._telefonszam_urlap.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        kezelo = KezeloGomb(self)
        kezelo.megse["command"] = self.destroy
        kezelo.ok["text"] = "mentés"
        kezelo.ok["command"] = self._ment
        kezelo.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _ment(self):
        telefonszam = self._telefonszam_urlap.export()
        if telefonszam:
            telefonszam.szemely = self._nev_valaszto.azonosito()
            if telefonszam.ment(self._kon):
                print("Bejegyzés mentve.")
            else:
                print("Nem sikerült elmenteni.")
        else:
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)


class TelefonTorloUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("személy", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("törlendő telefonszám", self._telefonszamok(), self)
        self._telefon_valaszto.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "törlés"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._torol
        kezelo.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.azonosito()
        return [Telefon(**telefon) for telefon in self._kon.select("telefon", szemely=szemely)]

    def _elerhetosegek(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())

    def _torol(self):
        idx = self._telefon_valaszto.idx
        if idx >= 0 and messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self):
            telefonszam = self._telefonszamok()[idx]
            if telefonszam.torol(self._kon):
                print("Bejegyzés törölve.")
            else:
                print("Nem sikerült törölni.")
            self._elerhetosegek(1)


class TelefonModositoUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("személy", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("módosítandó telefonszam", self._telefonszamok(), self)
        self._telefon_valaszto.valaszto.bind("<<ComboboxSelected>>", self._kiir_elerhetoseg)
        self._telefon_valaszto.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self)
        self._telefonszam_urlap.grid(row=2, column=0, sticky=W, ipadx=2, ipady=2)
        self._kiir_elerhetoseg(1)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "módosít"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._modosit
        kezelo.grid(row=3, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.azonosito()
        return [Telefon(**telefon) for telefon in self._kon.select("telefon", szemely=szemely)]

    def _elerhetosegek(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())
        self._kiir_elerhetoseg(1)

    def _kiir_elerhetoseg(self, event):
        idx = self._telefon_valaszto.idx
        telefonszam = self._telefonszamok()[idx] if idx >= 0 else Telefon()
        self._telefonszam_urlap.beallit(telefonszam)

    def _modosit(self):
        idx = self._telefon_valaszto.idx
        if idx >= 0:
            telefonszam = self._telefonszamok()[idx]
            telefonszam.adatok = self._telefonszam_urlap.export()
            if telefonszam:
                if telefonszam.ment(self._kon):
                    print("Bejegyzés módosítva.")
                else:
                    print("Nem sikerült módosítani.")
            else:
                messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            self._elerhetosegek(1)


class UjEmailUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("email hozzáadása", self._nevsor(), self)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self)
        self._emailcim_urlap.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        kezelo = KezeloGomb(self)
        kezelo.megse["command"] = self.destroy
        kezelo.ok["text"] = "mentés"
        kezelo.ok["command"] = self._ment
        kezelo.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _ment(self):
        emailcim = self._emailcim_urlap.export()
        if emailcim:
            emailcim.szemely = self._nev_valaszto.azonosito()
            if emailcim.ment(self._kon):
                print("Bejegyzés mentve.")
            else:
                print("Nem sikerült elmenteni.")
        else:
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)


class EmailTorloUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("személy", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("törlendő email-cím", self._emailcimek(), self)
        self._email_valaszto.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "törlés"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._torol
        kezelo.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _emailcimek(self):
        szemely = self._nev_valaszto.azonosito()
        return [Email(**email) for email in self._kon.select("email", szemely=szemely)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())

    def _torol(self):
        idx = self._email_valaszto.idx
        if idx >= 0 and messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self):
            emailcim = self._emailcimek()[idx]
            if emailcim.torol(self._kon):
                print("Bejegyzés törölve.")
            else:
                print("Nem sikerült törölni.")
            self._elerhetosegek(1)


class EmailModositoUrlap(Toplevel):
    def __init__(self, kon=None, **kw):
        super().__init__(**kw)
        self._kon = kon

        self._nev_valaszto = Valaszto("személy", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("módosítandó email-cím", self._emailcimek(), self)
        self._email_valaszto.valaszto.bind("<<ComboboxSelected>>", self._kiir_elerhetoseg)
        self._email_valaszto.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self)
        self._emailcim_urlap.grid(row=2, column=0, sticky=W, ipadx=2, ipady=2)
        self._kiir_elerhetoseg(1)

        kezelo = KezeloGomb(self)
        kezelo.megse["text"] = "vissza"
        kezelo.ok["text"] = "módosít"
        kezelo.megse["command"] = self.destroy
        kezelo.ok["command"] = self._modosit
        kezelo.grid(row=3, column=0, ipadx=2, ipady=2)

        self.grid()

    def _nevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.select("szemely")), key=repr)

    def _emailcimek(self):
        szemely = self._nev_valaszto.azonosito()
        return [Email(**email) for email in self._kon.select("email", szemely=szemely)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())
        self._kiir_elerhetoseg(1)

    def _kiir_elerhetoseg(self, event):
        idx = self._email_valaszto.idx
        emailcim = self._emailcimek()[idx] if idx >= 0 else Email()
        self._emailcim_urlap.beallit(emailcim)

    def _modosit(self):
        idx = self._email_valaszto.idx
        if idx >= 0:
            emailcim = self._emailcimek()[idx]
            emailcim.adatok = self._emailcim_urlap.export()
            if emailcim:
                if emailcim.ment(self._kon):
                    print("Bejegyzés módosítva.")
                else:
                    print("Nem sikerült módosítani.")
            else:
                messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            self._elerhetosegek(1)


if __name__ == "__main__":
    szulo = Tk()
    urlap = UjSzemelyUrlap(szulo)
    szulo.mainloop()

