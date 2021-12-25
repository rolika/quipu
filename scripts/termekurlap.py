from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from urlap import Valaszto
from szallito import Szallito
from termek import Termek
from anyag import Anyag


class TermekUrlap(Frame):
    """A termék egy árral rendelkező anyag."""
    def __init__(self, kon=None, master=None, **kw):
        """Az űrlap egy saját Frame()-ben jelenik meg.
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat
        master: szülő-widget (ha nincs megadva, saját új ablakban nyílik meg -> tesztelésre)
        **kw:   Frame() paraméterek testreszabáshoz"""
        super().__init__(master=master, **kw)
        self._kon = kon

        self._anyagvalaszto = Valaszto("anyag", self._anyagok(), self)
        self._anyagvalaszto.grid(row=0, column=0, columnspan=2, sticky=W, padx=2, pady=2)

        self._szallito_valaszto = Valaszto("szállító", self._szallitok(), self)
        self._szallito_valaszto.grid(row=1, column=0, columnspan=2, sticky=W, padx=2, pady=2)

        self._egysegar = StringVar()
        Label(self, text="egységár").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._egysegar, width=8).grid(row=2, column=1, sticky=W, padx=2, pady=2)

        self._megjegyzes = StringVar()
        Label(self, text="megjegyzés").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=3, column=1, sticky=W, padx=2, pady=2)
    
    @property
    def fokusz(self):
        """Az űrlap fókuszban lévő widget-je."""
        return self._anyagvalaszto.valaszto

    def export(self) -> Termek:
        """Űrlap tartalmának exportálása termékként."""
        return Termek(kon=self._kon,
            anyag=self._anyagvalaszto.elem.azonosito,
            szallito=self._szallito_valaszto.elem.azonosito,
            egysegar=self._egysegar.get(),
            megjegyzes=self._megjegyzes.get()
        )

    def beallit(self, termek:Termek) -> None:
        self._anyagvalaszto.valaszto.set(termek.anyag_teljes.listanezet())
        self._szallito_valaszto.valaszto.set(termek.szallito_teljes.listanezet())
        self._egysegar.set(termek.egysegar)
        self._megjegyzes.set(termek.megjegyzes)

    def _anyagok(self) -> list:
        """Anyagok felsorolása kiválasztáshoz."""
        assert self._kon
        return sorted(map(lambda anyag: Anyag(kon=self._kon, **anyag), self._kon.raktar.select("anyag")),
                      key=repr)

    def _szallitok(self) -> list:
        """Szállítók felsorolása kiválasztáshoz."""
        assert self._kon
        return sorted(map(lambda szallito: Szallito(kon=self._kon, **szallito), self._kon.kontakt.select("szallito")),
                      key=repr)


class UjTermekUrlap(simpledialog.Dialog):
    """Űrlap új termék létrehozására."""
    def __init__(self, szulo, kon=None) -> None:
        """Az űrlap egy simpledialog.Dialog példány.
        szulo:  szülő widget
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="Új termék létrehozása")
    
    def body(self, szulo):
        """Override Dialog.body - gui megjelenítése"""
        self._termekurlap = TermekUrlap(self._kon, self)
        self._termekurlap.pack(ipadx=2, ipady=2)
        return self._termekurlap.fokusz
    
    def validate(self) -> bool:
        """Override Dialog.validate - érvényes termék biztosítása"""
        termek = self._termekurlap.export()
        if not termek:
            messagebox.showwarning("Hiányos adat!", "Legalább az egységárat add meg!", parent=self)
            return False
        else:
            return True
    
    def apply(self) -> None:
        """Override Dialog.apply - termék mentése"""
        termek = self._termekurlap.export()
        print("{}: Bejegyzés mentve.".format(termek) if termek.ment(self._kon.raktar) else "Nem sikerült menteni.")
            
    


