from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from datetime import date
from urlap import Valaszto
from gyarto import Gyarto
from jelleg import Jelleg
from anyag import Anyag
from konstans import AnyagTipus


class AnyagUrlap(Frame):
    """Az anyag egy gyártó előállított anyag."""
    def __init__(self, kon=None, master=None, **kw):
        """Az űrlap egy saját Frame()-ben jelenik meg.
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat
        master: szülő-widget (ha nincs megadva, saját új ablakban nyílik meg -> tesztelésre)
        **kw:   Frame() paraméterek testreszabáshoz"""
        super().__init__(master=master, **kw)
        self._kon = kon

        self._nev = StringVar()
        self._tipus = StringVar()
        self._cikkszam = StringVar()
        self._leiras = StringVar()
        self._szin = StringVar()
        self._szinkod = StringVar()
        self._egyseg = StringVar()
        self._kiszereles_nev = StringVar()
        self._kiszereles = StringVar()
        self._csomagolas_nev = StringVar()
        self._csomagolas = StringVar()
        self._kritikus = StringVar()
        self._szallitasi_ido = StringVar()
        self._megjegyzes = StringVar()

        self._gyarto_valaszto = Valaszto("gyártó", self._gyartok(), self)
        self._gyarto_valaszto.grid(row=0, column=0, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="név").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._nev, width=32)
        self._fokusz.grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="típus").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        anyagtipusok = [anyag.value for anyag in AnyagTipus]
        OptionMenu(self, self._tipus, *anyagtipusok).grid(row=2, column=1, sticky=W, padx=2, pady=2)
        self._tipus.set(AnyagTipus.SZIG.value)

        Label(self, text="cikkszám").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._cikkszam, width=16).grid(row=3, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="leírás").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._leiras, width=32).grid(row=4, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="szín").grid(row=5, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._szin, width=16).grid(row=5, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="színkód").grid(row=6, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._szinkod, width=16).grid(row=6, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="egység").grid(row=7, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._egyseg, width=8).grid(row=7, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kiszerelés neve").grid(row=8, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kiszereles_nev, width=8).grid(row=8, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kiszerelés").grid(row=9, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kiszereles, width=8).grid(row=9, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="csomagolás neve").grid(row=10, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._csomagolas_nev, width=8).grid(row=10, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="csomagolás").grid(row=11, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._csomagolas, width=8).grid(row=11, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kritikus szint").grid(row=12, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kritikus, width=8).grid(row=12, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="szállítási idő").grid(row=13, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._szallitasi_ido, width=8).grid(row=13, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=14, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=14, column=1, sticky=W, padx=2, pady=2)

    @property
    def fokusz(self):
        return self._gyarto_valaszto

    
    def beallit(self, anyag:Anyag) -> None:
        """Adatokkal tölti fel az űrlapot.
        anyag:  anyag.Anyag csomó"""
        self._gyarto_valaszto.valaszto.set(self._gyarto(anyag).listanezet())
        self._nev.set(anyag.nev)
        self._tipus.set(anyag.tipus)
        self._cikkszam.set(anyag.cikkszam)
        self._leiras.set(anyag.leiras)
        self._szin.set(anyag.szin)
        self._szinkod.set(anyag.szinkod)
        self._egyseg.set(anyag.egyseg)
        self._kiszereles_nev.set(anyag.kiszereles_nev)
        self._kiszereles.set(anyag.kiszereles)
        self._csomagolas_nev.set(anyag.csomagolas_nev)
        self._csomagolas.set(anyag.csomagolas)
        self._kritikus.set(anyag.kritikus)
        self._szallitasi_ido.set(anyag.szallitasi_ido)
        self._megjegyzes.set(anyag.megjegyzes)

    def export(self) -> Anyag:
        """Beolvassa az űrlap kitöltött mezőit és Anyag csomót ad vissza belőlük."""
        return Anyag(kon=self._kon,
            gyarto = self._gyarto_valaszto.elem.azonosito,
            nev = self._nev.get(),
            tipus = self._tipus.get(),
            cikkszam = self._cikkszam.get(),
            leiras = self._leiras.get(),
            szin = self._szin.get(),
            szinkod = self._szinkod.get(),
            egyseg = self._egyseg.get(),
            kiszereles_nev = self._kiszereles_nev.get(),
            kiszereles = self._kiszereles.get(),
            csomagolas_nev = self._csomagolas_nev.get(),
            csomagolas = self._csomagolas.get(),
            kritikus = self._kritikus.get(),
            szallitasi_ido = self._szallitasi_ido.get(),
            megjegyzes = self._megjegyzes.get()
        )

    def _gyartok(self) -> list:
        """Gyártócégek felsorolása."""
        assert self._kon
        return sorted(map(lambda gyarto: Gyarto(kon=self._kon, **gyarto), self._kon.kontakt.select("gyarto")),
                      key=repr)
    
    def _gyarto(self, anyag:Anyag) -> Gyarto:
        """Ismert azonosítójú gyártó."""
        gyarto = self._kon.kontakt.select("gyarto", azonosito=anyag.gyarto).fetchone()
        return Gyarto(kon=self._kon, **gyarto)


class AruUrlap(Frame):
    """Az áru olyan termék, melynek ára van. Ha projektet is megadunk, akkor projektár(u) lesz."""
    def __init__(self, kon=None, master=None, **kw):
        """Az űrlap egy saját Frame()-ben jelenik meg.
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat
        master: szülő-widget (ha nincs megadva, saját új ablakban nyílik meg -> tesztelésre)
        **kw:   Frame() paraméterek testreszabáshoz"""
        super().__init__(master=master, **kw)
        self._kon = kon

        self._egysegar = StringVar()
        self._ervenyes = StringVar()
        self._megjegyzes = StringVar()

        self._termek_valaszto = Valaszto("termék", self._termekek(), self)
        self._termek_valaszto.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        self._projekt_valaszto = Valaszto("projekt", self._projektek(), self)
        self._projekt_valaszto.grid(row=1, column=0, sticky=W, padx=2, pady=2)

        Label(self, text="egységár").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._egysegar, width=10).grid(row=2, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="Ft/{}".format(self._mertekegyseg())).grid(row=2, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="érvényes").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._ervenyes, width=10).grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="éé-hh-nn").grid(row=3, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)

    @property
    def fokusz(self):
        return self._termek_valaszto

    def _termekek(self):
        """Termékek felsorolása."""
        assert self._kon
        return sorted(map(lambda anyag: Anyag(**anyag), self._kon.raktar.select("anyag")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _projektek(self):
        """Projektek (igazából jellegek) felsorolása."""
        return sorted(map(lambda jelleg: Jelleg(**jelleg), self._kon.projekt.select("jelleg")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _mertekegyseg(self):
        assert self._kon
        return "m2"


class UjAnyagUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon=None) -> None:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új anyag létrehozása")
    
    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._anyagurlap = AnyagUrlap(self._kon, self)
        self._anyagurlap.pack(ipadx=2, ipady=2)
    
    def validate(self) -> bool:
        """Override Dialog.validate - érvényes anyag biztosítása"""
        anyag = self._anyagurlap.export()
        if not anyag:
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet és az egységet add meg!", parent=self)
            return False
        if anyag.meglevo(self._kon.raktar):
            messagebox.showwarning("Az anyag már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True

    def apply(self) -> None:
        """Override Dialog.apply - anyag mentése"""
        anyag = self._anyagurlap.export()
        print("{}: Bejegyzés mentve.".format(anyag) if anyag.ment(self._kon.raktar) else "Nem sikerült menteni.")


class AnyagTorloUrlap(simpledialog.Dialog):
    """Űrlap meglévő anyag törlésére."""
    def __init__(self, szulo, kon=None) -> None:
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Anyag törlése")
    
    def body(self, szulo) -> Combobox:
        """Override Dialog.body - gui megjelenítése"""
        self._anyagvalaszto = Valaszto("anyag", self._anyagok(), self)
        self._anyagvalaszto.pack(ipadx=2, ipady=2)
        return self._anyagvalaszto.valaszto

    def validate(self) -> bool:
        """Override Dialog.validate - törlés előtti utolsó megerősítés"""
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!")
    
    def apply(self) -> None:
        """Override Dialog.apply - törlés végrehajtása"""
        anyag = self._anyagvalaszto.elem
        print("{}: Bejegyzés törölve.".format(anyag) if anyag.torol(self._kon.raktar) else "Nem sikerült törölni.")
    
    def _anyagok(self) -> list:
        """Az anyagok custom repr alapján abc-sorrendbe rakott listát készít."""
        return sorted(map(lambda anyag: Anyag(kon=self._kon, **anyag), self._kon.raktar.select("anyag")), key=repr)


class AnyagModositoUrlap(simpledialog.Dialog):
    """Űrlap meglévő anyag módosítására."""
    def __init__(self, szulo, kon=None) -> None:
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Anyag módosítása")
    
    def body(self, szulo) -> Combobox:
        """Override Dialog.body - gui megjelenítése"""
        self._anyagvalaszto = Valaszto("anyag", self._anyagok(), self)
        self._anyagvalaszto.pack(ipadx=2, ipady=2)
        self._anyagvalaszto.set_callback(self._megjelenit)

        self._anyagurlap = AnyagUrlap(self._kon, self)
        self._anyagurlap.pack(ipadx=2, ipady=2)

        self._megjelenit(1)

        return self._anyagvalaszto.valaszto

    def validate(self) -> bool:
        """Override Dialog.validate - érvényes anyag biztosítása"""
        anyag = self._anyagurlap.export()
        if not anyag:
            messagebox.showwarning("Hiányos adat!", "Legalább a nevet és az egységet add meg!", parent=self)
            return False
        if anyag.meglevo(self._kon.raktar):
            messagebox.showwarning("Az anyag már létezik!", "Különböztesd meg a megjegyzésben!", parent=self)
            return False
        return True
    
    def apply(self) -> None:
        """Override Dialog.apply - módosítás végrehajtása"""
        anyag = self._anyagvalaszto.elem
        anyag.adatok = self._anyagurlap.export()
        print("{}: Bejegyzés módosítva.".format(anyag) if anyag.ment(self._kon.raktar) else "Nem sikerült módosítani.")
    
    def _anyagok(self) -> list:
        """Az anyagok custom repr alapján abc-sorrendbe rakott listát készít."""
        return sorted(map(lambda anyag: Anyag(kon=self._kon, **anyag), self._kon.raktar.select("anyag")), key=repr)
    
    def _megjelenit(self, event):
        """Az anyag adatainak eseményvezérelt kijelzése az űrlap mezőibe."""
        self._anyagurlap.beallit(self._anyagvalaszto.elem or Anyag())


if __name__ == "__main__":
    app = AruUrlap()
    app.pack()
    app.mainloop()