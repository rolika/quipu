"""A Quipu személyekkel kapcsolatos űrlapjait tartalmazza."""


from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from urlap import TelefonszamUrlap, EmailcimUrlap, CimUrlap, Valaszto, SzemelyUrlap
from szemely import Szemely
from telefon import Telefon
from e_mail import Email
from cim import Cim
from szervezet import Szervezet
from kontakt import Kontakt
from vevo import Vevo
from szallito import Szallito
from gyarto import Gyarto
from konstans import VITYA, ROLI


class UjSzemelyUrlap(simpledialog.Dialog):
    """Új személy adatait beolvasó űrlap."""
    def __init__(self, szulo, kon=None) -> simpledialog.Dialog:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új személy felvitele")

    def body(self, szulo) -> Entry:
        """Override Dialog.body - gui megjelenítése"""
        self._szemelyurlap = SzemelyUrlap(self, self._kon)
        self._szemelyurlap.pack(ipadx=2, ipady=2)
        return self._szemelyurlap.fokusz

    def validate(self) -> bool:
        """Override Dialog.validate - személyi adatok ellenőrzése"""
        szemely = self._szemelyurlap.export()
        if not szemely:
            messagebox.showwarning("Hiányos adat!", "Legalább az egyik nevet add meg!", parent=self)
            return False
        if szemely.meglevo():
            messagebox.showwarning("A név már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True

    def apply(self) -> None:
        """Override Dialog.apply - személy mentése"""
        szemely = self._szemelyurlap.export()
        if szemely.ment():
            print("{}: Bejegyzés mentve.".format(szemely))
        else:  # adatbázis-hiba visszajelzése
            print("Nem sikerült elmenteni.")


class SzemelyTorloUrlap(simpledialog.Dialog):
    """Meglévő személy adatait törlő űrlap."""
    def __init__(self, szulo, kon=None) -> simpledialog.Dialog:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon
        super().__init__(szulo, title="Személy törlése")

    def body(self, szulo) -> Combobox:
        """Override Dialog.body - gui megjelenítése"""
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)
        return self._nev_valaszto.valaszto

    def validate(self) -> bool:
        """Override Dialog.validate - törlés előtti utolsó megerősítés"""
        szemely = self._nev_valaszto.elem
        if szemely.azonosito in (VITYA.azonosito, ROLI.azonosito):
            return False  # nem engedem törölni a speciális eseteket
        biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!", parent=self)
        return szemely and biztos

    def apply(self) -> None:
        """Override Dialog.apply - személy törlése"""
        szemely = self._nev_valaszto.elem
        self._kon.szemely.delete("telefon", szemely=szemely.azonosito)  # GDPR!
        self._kon.szemely.delete("email", szemely=szemely.azonosito)
        self._kon.szemely.delete("cim", szemely=szemely.azonosito)
        if szemely.torol():
            print("{}: Bejegyzés törölve.".format(szemely))
            self._nev_valaszto.beallit(Szemely.osszes(self._kon))
        else:
            print("Nem sikerült törölni.")


class SzemelyModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Személy módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._szemelyurlap = SzemelyUrlap(self, self._kon)
        self._szemelyurlap.pack(ipadx=2, ipady=2)
        self._megjelenit(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        if self._nev_valaszto.elem.azonosito in (VITYA.azonosito, ROLI.azonosito):
            return False  # nem engedem módosítani a speciális eseteket
        szemely = self._szemelyurlap.export()
        if not szemely:
            messagebox.showwarning("Hiányos adat!", "Legalább az egyik nevet add meg!", parent=self)
            return False
        if szemely.meglevo():
            messagebox.showwarning("A név már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True

    def apply(self):
        szemely = self._nev_valaszto.elem
        szemely.adatok = self._szemelyurlap.export()
        if szemely.ment():
            print("{}: Bejegyzés módosítva.".format(szemely))
        else:
            print("Nem sikerült módosítani.")

    def _megjelenit(self, event):
        self._szemelyurlap.beallit(self._nev_valaszto.elem or Szemely(kon=self._kon))


class UjTelefonUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Telefon.db = "szemely"
        super().__init__(szulo, title="Új telefonszám hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self, self._kon)
        self._telefonszam_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        telefonszam = self._telefonszam_urlap.export()
        if not telefonszam:
            messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
            return False
        return True

    def apply(self):
        telefonszam = self._telefonszam_urlap.export()
        telefonszam.szemely = self._nev_valaszto.elem.azonosito
        print("Bejegyzés mentve." if telefonszam.ment() else "Nem sikerült elmenteni.")


class TelefonTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Telefon.db = "szemely"
        super().__init__(szulo, title="Telefonszám törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenites)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("törlendő telefonszám", self._telefonszamok(), self)
        self._telefon_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        telefonszam = self._telefon_valaszto.elem
        if telefonszam:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return telefonszam and biztos  # rövidzárlat miatt a biztos nem értékelődik ki, ha a telefonszám nem igaz

    def apply(self):
        telefonszam = self._telefon_valaszto.elem
        print("Bejegyzés törölve." if telefonszam.torol() else "Nem sikerült törölni.")
        self._megjelenites(1)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.elem.azonosito
        return [Telefon(kon=self._kon, **telefon) for telefon in self._kon.szemely.select("telefon", szemely=szemely)]

    def _megjelenites(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())


class TelefonModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Telefon.db = "szemely"
        super().__init__(szulo, title="Telefonszám módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._telefon_valaszto = Valaszto("módosítandó telefonszam", self._telefonszamok(), self)
        self._telefon_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenites)
        self._telefon_valaszto.pack(ipadx=2, ipady=2)

        self._telefonszam_urlap = TelefonszamUrlap(self, self._kon)
        self._telefonszam_urlap.pack(ipadx=2, ipady=2)
        self._megjelenites(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._telefon_valaszto.elem:
            return False
        else:
            if not self._uj_telefonszam():
                messagebox.showwarning("Hiányos adat!", "Add meg a telefonszámot!", parent=self)
                return False
            else:
                return True

    def apply(self):
        print("Bejegyzés módosítva." if self._uj_telefonszam().ment() else "Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _telefonszamok(self):
        szemely = self._nev_valaszto.elem.azonosito
        return [Telefon(kon=self._kon, **telefon) for telefon in self._kon.szemely.select("telefon", szemely=szemely)]

    def _elerhetosegek(self, event):
        self._telefon_valaszto.beallit(self._telefonszamok())
        self._megjelenites(1)

    def _megjelenites(self, event):
        self._telefonszam_urlap.beallit(self._telefon_valaszto.elem or Telefon(kon=self._kon))

    def _uj_telefonszam(self):
        telefon = self._telefon_valaszto.elem
        if telefon:
            telefon.adatok = self._telefonszam_urlap.export()
        return telefon


class UjEmailUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Email.db = "szemely"
        super().__init__(szulo, title="Új email-cím hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self, self._kon)
        self._emailcim_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._emailcim_urlap.export():
            messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
            return False
        else:
            return True

    def apply(self):
        emailcim = self._emailcim_urlap.export()
        emailcim.szemely = self._nev_valaszto.elem.azonosito
        print("Bejegyzés mentve." if emailcim.ment() else "Nem sikerült elmenteni.")


class EmailTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Email.db = "szemely"
        super().__init__(szulo, title="Email-cím törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("törlendő email-cím", self._emailcimek(), self)
        self._email_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        emailcim = self._email_valaszto.elem
        if emailcim:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return emailcim and biztos  # rövidzárlat miatt a biztos nem értékelődik ki, ha az emailcím nem igaz

    def apply(self):
        emailcim = self._email_valaszto.elem
        print("Bejegyzés törölve." if emailcim.torol() else "Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _emailcimek(self):
        szemely = self._nev_valaszto.elem
        return [Email(kon=self._kon, **email) for email in self._kon.szemely.select("email", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())


class EmailModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Email.db = "szemely"
        super().__init__(szulo, title="Email-cím módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._email_valaszto = Valaszto("módosítandó email-cím", self._emailcimek(), self)
        self._email_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenites)
        self._email_valaszto.pack(ipadx=2, ipady=2)

        self._emailcim_urlap = EmailcimUrlap(self, self._kon)
        self._emailcim_urlap.pack(ipadx=2, ipady=2)
        self._megjelenites(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._email_valaszto.elem:
            return False
        else:
            if not self._uj_emailcim():
                messagebox.showwarning("Hiányos adat!", "Add meg az email-címet!", parent=self)
                return False
            else:
                return True

    def apply(self):
        print("Bejegyzés módosítva." if self._uj_emailcim().ment() else "Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _emailcimek(self):
        szemely = self._nev_valaszto.elem
        return [Email(kon=self._kon, **email) for email in self._kon.szemely.select("email", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._email_valaszto.beallit(self._emailcimek())
        self._megjelenites(1)

    def _megjelenites(self, event):
        self._emailcim_urlap.beallit(self._email_valaszto.elem or Email(kon=self._kon))

    def _uj_emailcim(self):
        email = self._email_valaszto.elem
        if email:
            email.adatok = self._emailcim_urlap.export()
        return email


class UjCimUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Cim.db = "szemely"
        super().__init__(szulo, title="Új cím hozzáadása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_urlap = CimUrlap(self, self._kon)
        self._cim_urlap.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._cim_urlap.export():
            messagebox.showwarning("Hiányos adat!", "Legalább a helységet add meg!", parent=self)
            return False
        return True

    def apply(self):
        cim = self._cim_urlap.export()
        cim.szemely = self._nev_valaszto.elem.azonosito
        print("Bejegyzés mentve." if cim.ment() else "Nem sikerült elmenteni.")


class CimTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Cim.db = "szemely"
        super().__init__(szulo, title="Cím törlése")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_valaszto = Valaszto("törlendő cím", self._cimek(), self)
        self._cim_valaszto.pack(ipadx=2, ipady=2)

        return self._nev_valaszto.valaszto

    def validate(self):
        cim = self._cim_valaszto.elem
        if cim:
            biztos = messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)
        return cim and biztos  # rövidzárlat miatt a biztos nem értékelődik ki, ha a cím nem igaz

    def apply(self):
        print("Bejegyzés törölve." if self._cim_valaszto.elem.torol() else "Nem sikerült törölni.")
        self._elerhetosegek(1)

    def _cimek(self):
        szemely = self._nev_valaszto.elem
        return [Cim(kon=self._kon, **cim) for cim in self._kon.szemely.select("cim", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._cim_valaszto.beallit(self._cimek())


class CimModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        Cim.db = "szemely"
        super().__init__(szulo, title="Cím módosítása")

    def body(self, szulo):
        self._nev_valaszto = Valaszto("név", Szemely.osszes(self._kon), self)
        self._nev_valaszto.valaszto.bind("<<ComboboxSelected>>", self._elerhetosegek)
        self._nev_valaszto.pack(ipadx=2, ipady=2)

        self._cim_valaszto = Valaszto("módosítandó cím", self._cimek(), self)
        self._cim_valaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenites)
        self._cim_valaszto.pack(ipadx=2, ipady=2)

        self._cim_urlap = CimUrlap(self, self._kon)
        self._cim_urlap.pack(ipadx=2, ipady=2)
        self._megjelenites(1)

        return self._nev_valaszto.valaszto

    def validate(self):
        if not self._cim_valaszto.elem:
            return False
        else:
            if not self._uj_cim():
                messagebox.showwarning("Hiányos adat!", "Legalább a helységet add meg!", parent=self)
                return False
            else:
                return True

    def apply(self):
        print("Bejegyzés módosítva." if self._uj_cim().ment() else "Nem sikerült módosítani.")
        self._elerhetosegek(1)

    def _cimek(self):
        szemely = self._nev_valaszto.elem
        return [Cim(kon=self._kon, **cim) for cim in self._kon.szemely.select("cim", szemely=szemely.azonosito)]

    def _elerhetosegek(self, event):
        self._cim_valaszto.beallit(self._cimek())
        self._megjelenites(1)

    def _megjelenites(self, event):
        self._cim_urlap.beallit(self._cim_valaszto.elem or Cim())

    def _uj_cim(self):
        cim = self._cim_valaszto.elem
        if cim:
            cim.adatok = self._cim_urlap.export()
        return cim


class UjKontaktUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Szervezet hozzárendelése")

    def body(self, szulo):
        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        vevo_fr = Frame(self)
        self._vevo = IntVar()
        self._vevo_cb = Checkbutton(vevo_fr, text="vevő", variable=self._vevo)
        self._vevo_cb.select()
        self._vevo_cb.pack(side=LEFT, ipadx=2, ipady=2)
        self._szallito = IntVar()
        Checkbutton(vevo_fr, text="szállító", variable=self._szallito).pack(side=LEFT, ipadx=2, ipady=2)
        self._gyarto = IntVar()
        Checkbutton(vevo_fr, text="gyártó", variable=self._gyarto).pack(side=BOTTOM, ipadx=2, ipady=2)
        vevo_fr.pack()

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").pack(ipadx=2, ipady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).pack(ipadx=2, ipady=2)

        return self._szemelyvalaszto

    def validate(self):
        return self._vevo.get() or self._szallito.get() or self._gyarto.get()

    def apply(self):
        kontakt = Kontakt(szemely=self._szemelyvalaszto.elem.azonosito,
                          szervezet=self._szervezetvalaszto.elem.azonosito,
                          megjegyzes=self._megjegyzes.get())
        if kontakt_azonosito := kontakt.ment(self._kon.kontakt):
            print("Bejegyzés mentve.")
        else:
            print("Nem sikerült elmenteni.")

        if self._vevo.get():
            vevo = Vevo(kon=self._kon, kontakt=kontakt_azonosito)
            if vevo.ment(self._kon.kontakt):
                print("Vevő mentve.")
            else:
                print("Nem sikerült elmenteni.")

        if self._szallito.get():
            szallito = Szallito(kon=self._kon, kontakt=kontakt_azonosito)
            if szallito.ment(self._kon.kontakt):
                print("Szállító mentve.")
            else:
                print("Nem sikerült elmenteni.")

        if self._gyarto.get():
            gyarto = Gyarto(kon=self._kon, kontakt=kontakt_azonosito)
            if gyarto.ment(self._kon.kontakt):
                print("Gyártó mentve.")
            else:
                print("Nem sikerült elmenteni.")

    def _szemelynevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.szemely.select("szemely")), key=repr)

    def _szervezetnevsor(self):
        szemelyazonosito = self._szemelyvalaszto.elem.azonosito
        szemelyhez_nem_rendelt_szervezetek = self._kon.szemely.execute("""
            SELECT * FROM szervezet WHERE azonosito NOT IN (SELECT szervezet FROM kontakt WHERE szemely = ?);
        """, (szemelyazonosito, ))
        return sorted(map(lambda szervezet: Szervezet(**szervezet), szemelyhez_nem_rendelt_szervezetek), key=repr)

    def _megjelenit(self, event):
        self._szervezetvalaszto.beallit(self._szervezetnevsor())


class KontaktTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Szervezet eltávolítása")

    def body(self, szulo):
        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        return self._szemelyvalaszto

    def validate(self):
        if self._szervezetvalaszto.elem:
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

        vevo = self._kon.kontakt.select("vevo", kontakt=kontakt.azonosito).fetchone()
        if vevo:
            vevo = Vevo(**vevo)
            if vevo.torol(self._kon.kontakt):
                print("Vevő törölve.")
            else:
                print("Nem sikerült a vevőt törölni.")

        szallito = self._kon.kontakt.select("szallito", kontakt=kontakt.azonosito).fetchone()
        if szallito:
            szallito = Szallito(**szallito)
            if szallito.torol(self._kon.kontakt):
                print("Szállító törölve.")
            else:
                print("Nem sikerült a szállítót törölni.")

        gyarto = self._kon.kontakt.select("gyarto", kontakt=kontakt.azonosito).fetchone()
        if gyarto:
            gyarto = Gyarto(**gyarto)
            if gyarto.torol(self._kon.kontakt):
                print("Gyártó törölve.")
            else:
                print("Nem sikerült a gyártót törölni.")

    def _szemelynevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.szemely.select("szemely")), key=repr)

    def _szervezetnevsor(self):
        szemelyazonosito = self._szemelyvalaszto.elem.azonosito
        szemelyhez_rendelt_szervezetek = self._kon.szemely.execute("""
            SELECT * FROM szervezet WHERE azonosito IN (SELECT szervezet FROM kontakt WHERE szemely = ?);
        """, (szemelyazonosito, ))
        return sorted(map(lambda szervezet: Szervezet(**szervezet), szemelyhez_rendelt_szervezetek), key=repr)

    def _megjelenit(self, event):
        self._szervezetvalaszto.beallit(self._szervezetnevsor())


class KontaktModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None):
        self._kon = kon
        super().__init__(szulo, title="Szervezet módosítása")

    def body(self, szulo):
        self._szemelyvalaszto = Valaszto("személy", self._szemelynevsor(), self)
        self._szemelyvalaszto.valaszto.bind("<<ComboboxSelected>>", self._megjelenit)
        self._szemelyvalaszto.pack(ipadx=2, ipady=2)

        self._szervezetvalaszto = Valaszto("szervezet", self._szervezetnevsor(), self)
        self._szervezetvalaszto.valaszto.bind("<<ComboboxSelected>>", self._reszletek)
        self._szervezetvalaszto.pack(ipadx=2, ipady=2)

        self._modszervezetvalaszto = Valaszto("módosítás erre", self._modszervezetnevsor(), self)
        self._modszervezetvalaszto.pack(ipadx=2, ipady=2)

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").pack(ipadx=2, ipady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).pack(ipadx=2, ipady=2)

        self._megjelenit(1)

        return self._szemelyvalaszto

    def validate(self):
        return True

    def apply(self):
        szemely = self._szemelyvalaszto.elem.azonosito
        szervezet = self._szervezetvalaszto.elem.azonosito
        modszervezet = self._modszervezetvalaszto.elem.azonosito
        megjegyzes = self._megjegyzes.get()
        kontakt_id = self._kon.kontakt.select("kontakt", "azonosito", szemely=szemely, szervezet=szervezet, logic="AND")
        kontakt_id = kontakt_id.fetchone()["azonosito"]
        kontakt = Kontakt(azonosito=kontakt_id, szemely=szemely, szervezet=modszervezet, megjegyzes=megjegyzes)
        if kontakt.ment(self._kon.kontakt):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani.")

    def _szemelynevsor(self):
        return sorted(map(lambda szemely: Szemely(**szemely), self._kon.szemely.select("szemely")), key=repr)

    def _szervezetnevsor(self):
        szemelyazonosito = self._szemelyvalaszto.elem.azonosito
        szemelyhez_rendelt_szervezetek = self._kon.szemely.execute("""
            SELECT *
            FROM szervezet
            WHERE azonosito IN (
                SELECT szervezet
                FROM kontakt
                WHERE szemely = ?
            );
        """, (szemelyazonosito, ))
        return sorted(map(lambda szervezet: Szervezet(**szervezet), szemelyhez_rendelt_szervezetek), key=repr)

    def _modszervezetnevsor(self):
        szemelyazonosito = self._szemelyvalaszto.elem.azonosito
        szemelyhez_nem_rendelt_szervezetek = self._kon.szemely.execute("""
            SELECT *
            FROM szervezet
            WHERE azonosito NOT IN (
                SELECT szervezet
                FROM kontakt
                WHERE szemely = ?
            );
        """, (szemelyazonosito, ))
        return sorted(map(lambda szervezet: Szervezet(**szervezet), szemelyhez_nem_rendelt_szervezetek), key=repr)

    def _megjelenit(self, event):
        self._szervezetvalaszto.beallit(self._szervezetnevsor())
        self._modszervezetvalaszto.beallit(self._modszervezetnevsor())
        self._reszletek(1)

    def _reszletek(self, event):
        szemely = self._szemelyvalaszto.elem.azonosito
        szervezet = self._szervezetvalaszto.elem.azonosito
        megjegyzes = self._kon.kontakt.select("kontakt",
                                              "megjegyzes",
                                              szemely=szemely,
                                              szervezet=szervezet,
                                              logic="AND").fetchone()
        self._megjegyzes.set(megjegyzes["megjegyzes"])


if __name__ == "__main__":
    c = CimUrlap()
    c.pack()
    c.mainloop()
    print(c.export())
