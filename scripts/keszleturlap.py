from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from urlap import Valaszto


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
    
    def validate(self) -> bool:
        """Override Dialog.validate - érvényes készlet biztosítása"""
    
    def apply(self) -> None:
        """Override Dialog.apply - készlet mentése"""


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
    
    def validate(self) -> bool:
        """Override Dialog.validate - törlés előtti utolsó megerősítés"""
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN és MINDEN adata törlődik!")
    
    def apply(self) -> None:
        """Override Dialog.apply - törlés végrehajtása"""


class KeszletModositoUrlap(simpledialog.Dialog):
    """Űrlap meglévő készlet közvetlen módosítására."""
    def __init__(self, szulo, kon=None) -> None:
        self._kon = kon  # super() előtt kell legyen
        super().__init__(szulo, title="készlet módosítása")
    
    def body(self, szulo) -> Combobox:
        """Override Dialog.body - gui megjelenítése"""
    
    def validate(self) -> bool:
        """Override Dialog.validate - érvényes termék biztosítása"""
    
    def apply(self) -> None:
        """Override Dialog.apply - módosítás végrehajtása"""