from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from form.urlap import TelefonszamUrlap, EmailcimUrlap, CimUrlap, Valaszto
from csomok.szervezet import Szervezet
from csomok.telefon import Telefon
from csomok.e_mail import Email
from csomok.cim import Cim
from csomok.szemely import Szemely
from csomok.kontakt import Kontakt
from konstans import MAGANSZEMELY, WEVIK


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
        if szervezet.meglevo(self._kon.szervezet):
            messagebox.showwarning("Hiba!", "Ez a szervezet már szerepel az adatbázisban.")
            return False
        return True

    def apply(self):
        szervezet = self._szervezeturlap.export()
        if szervezet.ment(self._kon.szervezet):
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
        if szervezet.azonosito in (MAGANSZEMELY.azonosito, WEVIK.azonosito):
            return False  # nem engedem törölni a speciális eseteket
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)
        return szervezet and biztos

    def apply(self):
        szervezet = self._nev_valaszto.elem
        self._kon.szervezet.delete("telefon", szervezet=szervezet.azonosito)
        self._kon.szervezet.delete("email", szervezet=szervezet.azonosito)
        self._kon.szervezet.delete("cim", szervezet=szervezet.azonosito)
        self._kon.szervezet.delete("kontakt", szervezet=szervezet.azonosito)
        if szervezet.torol(self._kon.szervezet):
            print("{}: Bejegyzés törölve.".format(szervezet))
            self._nev_valaszto.beallit(self._nevsor())
        else:
            print("Nem sikerült törölni.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)


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
        if self._nev_valaszto.elem.azonosito == MAGANSZEMELY.azonosito:
            return False  # nem engedem módosítani a speciális esetet
        szervezet = self._szervezeturlap.export()
        if not szervezet:
            messagebox.showwarning("Hiányos adat!", "Legalább a rövid nevet add meg!", parent=self)
            return False
        if szervezet.meglevo(self._kon.szervezet):
            messagebox.showwarning("Hiba!", "Ez a szervezet már szerepel az adatbázisban.", parent=self)
            return False
        return True

    def apply(self):
        szervezet = self._nev_valaszto.elem
        szervezet.adatok = self._szervezeturlap.export()
        if szervezet.ment(self._kon.szervezet):
            print("{}: Bejegyzés módosítva.".format(szervezet))
        else:
            print("Nem sikerült módosítani.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _megjelenit(self, event):
        self._szervezeturlap.beallit(self._nev_valaszto.elem or Szervezet())


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
        if self._nev_valaszto.elem.azonosito == MAGANSZEMELY.azonosito:
            return False  # nem engedem módosítani a speciális esetet
        self._telefonszam = self._telefonszam_urlap.export()
        if not self._telefonszam:
            messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
            return False
        return True

    def apply(self):
        self._telefonszam.szervezet = self._nev_valaszto.elem.azonosito
        if self._telefonszam.ment(self._kon.szervezet):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)


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
        if self._telefonszam:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return self._telefonszam and biztos

    def apply(self):
        if self._telefonszam.torol(self._kon.szervezet):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _telefonszamok(self):
        szervezet = self._nev_valaszto.elem
        return [Telefon(**telefon) for telefon in self._kon.szervezet.select("telefon", szervezet=szervezet.azonosito)]

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
        if not self._telefon_valaszto.elem:
            return False
        else:
            self._telefonszam = self._uj_telefonszam()
            if not self._telefonszam:
                messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
                return False
            else:
                return True

    def apply(self):
        if self._telefonszam.ment(self._kon.szervezet):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _telefonszamok(self):
        szervezet = self._nev_valaszto.elem
        return [Telefon(**telefon) for telefon in self._kon.szervezet.select("telefon", szervezet=szervezet.azonosito)]

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
        if self._nev_valaszto.elem.azonosito == MAGANSZEMELY.azonosito:
            return False  # nem engedem módosítani a speciális esetet
        self._emailcim = self._emailcim_urlap.export()
        if not self._emailcim:
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            return False
        return True

    def apply(self):
        self._emailcim.szervezet = self._nev_valaszto.elem.azonosito
        if self._emailcim.ment(self._kon.szervezet):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)


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
        if self._emailcim:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return self._emailcim and biztos

    def apply(self):
        if self._emailcim.torol(self._kon.szervezet):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _emailcimek(self):
        szervezet = self._nev_valaszto.elem
        return [Email(**email) for email in self._kon.szervezet.select("email", szervezet=szervezet.azonosito)]

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
        if not self._email_valaszto.elem:
            return False
        else:
            self._emailcim = self._uj_emailcim()
            if not self._emailcim:
                messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
                return False
            else:
                return True

    def apply(self):
        if self._emailcim.ment(self._kon.szervezet):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _emailcimek(self):
        szervezet = self._nev_valaszto.elem
        return [Email(**email) for email in self._kon.szervezet.select("email", szervezet=szervezet.azonosito)]

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


class UjCimUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._cim = None
        super().__init__(szulo, title="Új cím hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_urlap = CimUrlap(self)
        self._cim_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        if self._nev_valaszto.elem.azonosito == MAGANSZEMELY.azonosito:
            return False  # nem engedem módosítani a speciális esetet
        self._cim = self._cim_urlap.export()
        if not self._cim:
            messagebox.showwarning("Hiányos adat!", "Legalább a helységet add meg!", parent=self)
            return False
        return True

    def apply(self):
        self._cim.szervezet = self._nev_valaszto.elem.azonosito
        if self._cim.ment(self._kon.szervezet):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)


class CimTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._cim = None
        super().__init__(szulo, title="Cím törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_valaszto = Valaszto("törlendő cím", self._cimek(), self)
        self._cim_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        self._cim = self._cim_valaszto.elem
        if self._cim:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return self._cim and biztos

    def apply(self):
        if self._cim.torol(self._kon.szervezet):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _cimek(self):
        szervezet = self._nev_valaszto.elem
        return [Cim(**cim) for cim in self._kon.szervezet.select("cim", szervezet=szervezet.azonosito)]

    def _elerhetosegek(self, event):
        self._cim_valaszto.beallit(self._cimek())


class CimModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        self._cim = None
        super().__init__(szulo, title="Cím módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", self._nevsor(), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_valaszto = Valaszto("módosítandó cím", self._cimek(), self)
        self._cim_valaszto.valaszto.bind("<<ComboboxSelected>>", self._kiir_elerhetoseg)
        self._cim_valaszto.pack(ipadx=2, ipady=2)

        self._cim_urlap = CimUrlap(self)
        self._cim_urlap.pack(ipadx=2, ipady=2)
        self._kiir_elerhetoseg(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._cim_valaszto.elem:
            return False
        else:
            self._cim = self._uj_cim()
            if not self._cim:
                messagebox.showwarning("Hiányos adat!", "Legalább a helységet add meg!", parent=self)
                return False
            else:
                return True

    def apply(self):
        if self._cim.ment(self._kon.szervezet):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _nevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _cimek(self):
        szervezet = self._nev_valaszto.elem
        return [Cim(**cim) for cim in self._kon.szervezet.select("cim", szervezet=szervezet.azonosito)]

    def _elerhetosegek(self, event):
        self._cim_valaszto.beallit(self._cimek())
        self._kiir_elerhetoseg(1)

    def _kiir_elerhetoseg(self, event):
        self._cim_urlap.beallit(self._cim_valaszto.elem or Cim())

    def _uj_cim(self):
        cim = self._cim_valaszto.elem
        if cim:
            cim.adatok = self._cim_urlap.export()
        return cim


class UjKontaktUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Kontaktszemély hozzárendelése")

    def body(self, szulo):
        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").pack(ipadx=2, ipady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).pack(ipadx=2, ipady=2)

        return self._szervezetvalaszto

    def validate(self):
        return True

    def apply(self):
        kontakt = Kontakt(szemely=self._szemelyvalaszto.elem.azonosito,
                          szervezet=self._szervezetvalaszto.elem.azonosito,
                          megjegyzes=self._megjegyzes.get())
        if kontakt.ment(self._kon.kontakt):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

    def _szervezetnevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _szemelynevsor(self):
        szervezetazonosito = self._szervezetvalaszto.elem.azonosito
        szervezethez_nem_rendelt_szemelyek = self._kon.szervezet.execute("""
            SELECT * FROM szemely WHERE azonosito NOT IN (SELECT szemely FROM kontakt WHERE szervezet = ?);
        """, (szervezetazonosito, ))
        return sorted(map(lambda szemely: Szemely(**szemely), szervezethez_nem_rendelt_szemelyek), key=repr)

    def _megjelenit(self, event):
        self._szemelyvalaszto.beallit(self._szemelynevsor())


class KontaktTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Kontaktszemély eltávolítása")

    def body(self, szulo):
        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        return self._szervezetvalaszto

    def validate(self):
        if self._szemelyvalaszto.elem:
            return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        else:
            return False

    def apply(self):
        kontakt = Kontakt(**(self._kon.kontakt.select("kontakt", logic="AND",
                                                       szemely=self._szemelyvalaszto.elem.azonosito,
                                                       szervezet=self._szervezetvalaszto.elem.azonosito).fetchone()))
        if kontakt.torol(self._kon.kontakt):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni.")

    def _szervezetnevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _szemelynevsor(self):
        szervezetazonosito = self._szervezetvalaszto.elem.azonosito
        szervezethez_rendelt_szemelyek = self._kon.szervezet.execute("""
            SELECT * FROM szemely WHERE azonosito IN (SELECT szemely FROM kontakt WHERE szervezet = ?);
        """, (szervezetazonosito, ))
        return sorted(map(lambda szemely: Szemely(**szemely), szervezethez_rendelt_szemelyek), key=repr)

    def _megjelenit(self, event):
        self._szemelyvalaszto.beallit(self._szemelynevsor())


class KontaktModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Kontaktszemély módosítása")

    def body(self, szulo):
        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.set_callback(self._megjelenit)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.set_callback(self._reszletek)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        self._modszemelyvalaszto = Valaszto("személy", self._modszemelynevsor(), self)
        self._modszemelyvalaszto.pack(ipadx=2, ipady=2)

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").pack(ipadx=2, ipady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).pack(ipadx=2, ipady=2)

        self._megjelenit(1)

        return self._szervezetvalaszto

    def validate(self):
        return True

    def apply(self):
        szervezet = self._szervezetvalaszto.elem.azonosito
        szemely = self._szemelyvalaszto.elem.azonosito
        modszemely = self._modszemelyvalaszto.elem.azonosito
        megjegyzes = self._megjegyzes.get()
        kontakt_id = self._kon.kontakt.select("kontakt", "azonosito", szemely=szemely, szervezet=szervezet, logic="AND")
        kontakt_id = kontakt_id.fetchone()["azonosito"]
        kontakt = Kontakt(azonosito=kontakt_id, szemely=modszemely, szervezet=szervezet, megjegyzes=megjegyzes)
        if kontakt.ment(self._kon.kontakt):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")

    def _szervezetnevsor(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._kon.szervezet.select("szervezet")), key=repr)

    def _szemelynevsor(self):
        szervezetazonosito = self._szervezetvalaszto.elem.azonosito
        szervezethez_rendelt_szemelyek = self._kon.szervezet.execute("""
            SELECT * 
            FROM szemely 
            WHERE azonosito IN (
                SELECT szemely FROM kontakt WHERE szervezet = ?
            );
        """, (szervezetazonosito, ))
        return sorted(map(lambda szemely: Szemely(**szemely), szervezethez_rendelt_szemelyek), key=repr)

    def _modszemelynevsor(self):
        szervezetazonosito = self._szervezetvalaszto.elem.azonosito
        szervezethez_nem_rendelt_szemelyek = self._kon.szervezet.execute("""
            SELECT * 
            FROM szemely 
            WHERE azonosito NOT IN (
                SELECT szemely 
                FROM kontakt 
                WHERE szervezet = ?
            );
        """, (szervezetazonosito, ))
        return sorted(map(lambda szemely: Szemely(**szemely), szervezethez_nem_rendelt_szemelyek), key=repr)

    def _megjelenit(self, event):
        self._szemelyvalaszto.beallit(self._szemelynevsor())
        self._modszemelyvalaszto.beallit(self._modszemelynevsor())
        self._reszletek(1)

    def _reszletek(self, event):
        szemely = self._szemelyvalaszto.elem.azonosito
        szervezet=self._szervezetvalaszto.elem.azonosito
        megjegyzes = self._kon.kontakt.select("kontakt", 
                                              "megjegyzes", 
                                              szemely=szemely, 
                                              szervezet=szervezet, 
                                              logic="AND").fetchone()
        self._megjegyzes.set(megjegyzes["megjegyzes"])


if __name__ == "__main__":
    sz = SzervezetUrlap()
    sz.pack()
    sz.mainloop()
