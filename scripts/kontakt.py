import dolog
from konstans import Kulcs


class Kontakt(dolog.Dolog):
    """Kontaktszemély megvalósítása"""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "szemely": 0,
                "szervezet": 0,
                "beosztas": "",
                "megjegyzes": ""
            }
        self._tabla = "kontakt"
        self._nev = ""
        self._ceg = ""
    
    def __str__(self):
        return "{}{}".format(self._nev, self._nullazo(self._ceg))
    
    def __repr__(self):
        return self._ascii_rep(str(self))
    
    def __bool__(self):
        return True
    
    @property
    def adatok(self):
        return self._adatok
    
    @adatok.setter
    def adatok(self, kontakt):
        self._adatok["szemely"] = kontakt.szemely
        self._adatok["szervezet"] = kontakt.szervezet
        self._adatok["beosztas"] = kontakt.beosztas
        self._adatok["megjegyzes"] = kontakt.megjegyzes
    
    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")

    @property
    def beosztas(self):
        return self._adatok.get("beosztas")
    
    @property
    def nev(self):
        return self._nev
    
    @nev.setter
    def nev(self, szemely):
        self._nev = szemely.listanezet()
    
    @property
    def ceg(self):
        return self._ceg
    
    @ceg.setter
    def ceg(self, szervezet):
        self._ceg = "" if szervezet.azonosito == Kulcs.MAGANSZEMELY.kulcs else str(szervezet)
    
    def listanezet(self):
        return str(self)