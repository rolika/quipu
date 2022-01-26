from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from keszlet import Keszlet
from termek import Termek
from urlap import Valaszto


class KeszletUrlap(Frame):
    """Készlet egy rektáron lévő termék mennyisége."""
    def __init__(self, kon=None, master=None, uj=True, **kw):
        """Az űrlap egy saját Frame()-ben jelenik meg.
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat
        master: szülő-widget (ha nincs megadva, saját új ablakban nyílik meg -> tesztelésre)
        uj:     új készlet (true) vagy meglévő készlet módosítása (false)
        **kw:   Frame() paraméterek testreszabáshoz"""
        super().__init__(master=master, **kw)
        self._kon = kon
        self._uj = uj

        if self._uj:
            cim = "termék"
            valasztek = self._termekek
        else:
            cim = "készlet"
            valasztek = self._keszletek

        self.termekvalaszto = Valaszto(cim, valasztek(), self)
        self.termekvalaszto.grid(row=0, column=0, columnspan=2, sticky=W, padx=2, pady=2)

        self._mennyiseg = StringVar()
        Label(self, text="mennyiség").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._mennyiseg, width=8).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self._erkezett = StringVar()
        Label(self, text="érkezett").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._erkezett, width=8).grid(row=2, column=1, sticky=W, padx=2, pady=2)

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=3, column=1, sticky=W, padx=2, pady=2)
    
    @property
    def fokusz(self):
        """Az űrlap fókuszban lévő widget-je."""
        return self.termekvalaszto.valaszto

    def export(self) -> Keszlet:
        """Űrlap tartalmának exportálása készletként."""
        try:
            mennyiseg = float(self._mennyiseg.get())
        except ValueError:
            mennyiseg = 0.0
        if self._uj:
            return Keszlet(kon=self._kon, termek=self.termekvalaszto.elem.azonosito, mennyiseg=mennyiseg, erkezett=self._erkezett.get(), megjegyzes=self._megjegyzes.get())
        else:
            modositando = self.termekvalaszto.elem
            modositando.mennyiseg = mennyiseg
            modositando.erkezett = self._erkezett.get()
            modositando.megjegyzes = self._megjegyzes.get()
            return modositando

    def beallit(self, keszlet:Keszlet) -> None:
        self.termekvalaszto.valaszto.set(Termek.adatbazisbol(self._kon, keszlet.termek).listanezet())
        self._mennyiseg.set(keszlet.mennyiseg)
        self._erkezett.set(keszlet.erkezett)
        self._megjegyzes.set(keszlet.megjegyzes)
    
    def _termekek(self) -> list:
        """Termékek felsorolása kiválasztáshoz."""
        assert self._kon
        return sorted(map(lambda termek: Termek(kon=self._kon, **termek), self._kon.raktar.select("termek")),
                      key=repr)
    
    def _keszletek(self) -> list:
        """Meglévő készletek felsorolása kiválasztáshoz."""
        assert self._kon
        keszletek = self._kon.raktar.execute("""
        SELECT keszlet.*
        FROM keszlet, termek
        ON keszlet.termek = termek.azonosito;
        """)
        return sorted(map(lambda keszlet: Keszlet(kon=self._kon, **keszlet), keszletek), key=repr)


class UjKeszletUrlap(simpledialog.Dialog):
    """Űrlap új készlet létrehozására."""
    def __init__(self, szulo, kon=None) -> None:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új készlet létrehozása")
    
    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._keszleturlap = KeszletUrlap(self._kon, self)
        self._keszleturlap.pack(ipadx=2, ipady=2)
        return self._keszleturlap.fokusz

    def validate(self) -> bool:
        """Override Dialog.validate - érvényes készlet biztosítása"""
        keszlet = self._keszleturlap.export()
        if keszlet.mennyiseg < 0:
            messagebox.showwarning("Rossz adat!", "A mennyiség legalább 0!", parent=self)
            return False
        else:
            return True
    
    def apply(self) -> None:
        """Override Dialog.apply - készlet mentése"""
        keszlet = self._keszleturlap.export()
        print("{}: Bejegyzés mentve.".format(keszlet) if keszlet.ment(self._kon.raktar) else "Nem sikerült menteni.")


class KeszletTorloUrlap(simpledialog.Dialog):
    """Űrlap meglévő készlet törlésére."""
    def __init__(self, szulo, kon=None) -> None:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Készlet törlése")
    
    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._keszletvalaszto = Valaszto("készlet", self._keszletek(), self)
        self._keszletvalaszto.pack(ipadx=2, ipady=2)
        return self._keszletvalaszto
    
    def validate(self) -> bool:
        """Override Dialog.validate - törlés előtti utolsó megerősítés"""
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!")
    
    def apply(self) -> None:
        """Override Dialog.apply - törlés végrehajtása"""
        keszlet = self._keszletvalaszto.elem
        print("{}: Bejegyzés törölve.".format(keszlet) if keszlet.torol(self._kon.raktar) else "Nem sikerült törölni.")
    
    def _keszletek(self):
        """A készletekből custom repr alapján abc-sorrendbe rakott listát készít."""
        return sorted(map(lambda keszlet: Keszlet(kon=self._kon, **keszlet), self._kon.raktar.select("keszlet")), key=repr)


class KeszletModositoUrlap(simpledialog.Dialog):
    """Űrlap meglévő készlet közvetlen módosítására."""
    def __init__(self, szulo, kon=None) -> None:
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="készlet módosítása")
    
    def body(self, szulo) -> Combobox:
        """Override Dialog.body - gui megjelenítése"""
        self._keszleturlap = KeszletUrlap(self._kon, self, uj=False)
        self._keszleturlap.termekvalaszto.set_callback(self._megjelenit)
        self._keszleturlap.pack(ipadx=2, ipady=2)
        self._megjelenit(1)
        return self._keszleturlap.fokusz
    
    def validate(self) -> bool:
        """Override Dialog.validate - érvényes készlet biztosítása"""
        keszlet = self._keszleturlap.export()
        if keszlet.mennyiseg < 0:
            messagebox.showwarning("Rossz adat!", "A mennyiség legalább 0!", parent=self)
            return False
        else:
            return True
    
    def apply(self) -> None:
        """Override Dialog.apply - módosítás végrehajtása"""
        keszlet = self._keszleturlap.export()
        print("{}: Bejegyzés módosítva.".format(keszlet) if keszlet.ment(self._kon.raktar) else "Nem sikerült módosítani.")
    
    def _megjelenit(self, event):
        """A készlet adatainak eseményvezérelt kijelzése az űrlap mezőibe."""
        self._keszleturlap.beallit(self._keszleturlap.termekvalaszto.elem or Keszlet())