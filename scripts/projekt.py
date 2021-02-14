from dolog import Dolog
from konstans import PROJEKT_NAGYSAGREND


class Projekt(Dolog):
    """Projekt megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "ev": self._aktualis_ev(),
                "szam": 0,
                "gyakorisag": 0,
                "megjegyzes": ""
            }
        self._tabla = "projekt"
        self._elvalaszto = "/"

    def __bool__(self):
        """ A projekt meghatározott, ha adott a megnevezése."""
        return bool(self.megnevezes)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, projekt):
        self._adatok["megnevezes"] = projekt.megnevezes
        self._adatok["ev"] = projekt.ev
        self._adatok["szam"] = projekt.szam
        self._adatok["gyakorisag"] = projekt.gyakorisag
        self._adatok["megjegyzes"] = projekt.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")
    
    @property
    def ev(self):
        return self._adatok.get("ev")
    
    @ev.setter
    def ev(self, evszam):
        self._adatok["ev"] = evszam
    
    @property
    def szam(self):
        return self._adatok.get("szam")
    
    @szam.setter
    def szam(self, projektszam):
        self._adatok["szam"] = projektszam

    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")
    
    @gyakorisag.setter
    def gyakorisag(self, ertek):
        self._adatok["gyakorisag"] = ertek
    
    @property
    def elvalaszto(self):
        return self._elvalaszto
    
    @elvalaszto.setter
    def elvalaszto(self, jel):
        self._elvalaszto = jel
    
    @property
    def projektszam(self):
        """Projektszám ábrázolása:
        - emberi használatra: pl. 21/13 (mint szöveg)
        - filenévnek, sorbarendezéshez: 21_013 (mint szöveg)
        """
        if self._elvalaszto == "/":
            formatum = "{}{}{}"
        elif self._elvalaszto == "_":
            formatum = "{{}}{{}}{{:0{}}}".format(PROJEKT_NAGYSAGREND)
        return formatum.format(self.ev, self._elvalaszto, self.szam)

    def hozzaer(self):
        self._adatok["gyakorisag"] += 1
    

