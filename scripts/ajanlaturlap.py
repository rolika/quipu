from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from datetime import date
from urlap import Valaszto
from projekt import Projekt
from munkaresz import Munkaresz


class UjAjanlatUrlap(simpledialog.Dialog):
    def __init__(self, szulo,
                 ajanlat_kon=None,
                 szemely_kon=None,
                 szervezet_kon=None,
                 kontakt_kon=None,
                 projekt_kon=None):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Új ajánlat(kérés) rögzítése")

        self._projekt_valaszto = Valaszto("projekt", self._projektek(), self)
        self._projekt_valaszto.valaszto.bind("<<ComboboxSelected>>", self._munkaresz_megjelenit)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)

        self._munkaresz_valaszto = Valaszto("munkarész", self._munkareszek(), self)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)

        self._kontakt_valaszto = Valaszto("ajánlatkérő", self._kontaktszemelyek(), self)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)
    
    def body(self, szulo):
        pass

    def validate(self):
        return True
    
    def apply(self):
        pass

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._projekt_kon.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _munkareszek(self):
        projekt = self._projekt_valaszto.elem
        return sorted(map(lambda munkaresz: Munkaresz(**munkaresz),
                          self._projekt_kon.select("munkaresz", projekt=projekt.azonosito)), key=repr)

    def _munkaresz_megjelenit(self, event):
        self._munkaresz_valaszto.beallit(self._munkareszek())


class AjanlatTorloUrlap(simpledialog.Dialog):
    def __init__(self, szulo,
                 ajanlat_kon=None,
                 szemely_kon=None,
                 szervezet_kon=None,
                 kontakt_kon=None,
                 projekt_kon=None):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Ajánlat(kérés) törlése")


class AjanlatModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo,
                 ajanlat_kon=None,
                 szemely_kon=None,
                 szervezet_kon=None,
                 kontakt_kon=None,
                 projekt_kon=None):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Ajánlat(kérés) módosítása")