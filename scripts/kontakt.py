from csomo import Csomo
from szemely import Szemely
from szervezet import Szervezet
from konstans import MAGANSZEMELY


class Kontakt(Csomo):
    """Kontaktszemély megvalósítása. Összetett csomó, több külső kulcsra támaszkodik."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "szemely": 0,
                "szervezet": 0,
                "megjegyzes": ""
            }
        self._tabla = "kontakt"
    
    def __str__(self):
        return self.listanezet()
    
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
        self._adatok["megjegyzes"] = kontakt.megjegyzes
    
    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")
    
    def listanezet(self):
        assert self._kon
        szemely = self._kon.szemely.select("szemely", azonosito=self.szemely).fetchone()
        szemely = Szemely(kon=self._kon, **szemely)
        szervezet = self._kon.szervezet.select("szervezet", azonosito=self.szervezet).fetchone()
        szervezet = Szervezet(kon=self._kon, **szervezet)
        if szervezet == MAGANSZEMELY:  # __eq__ használata
            szervezet.rovidnev = ""
        return "{nev}{ceg}".format(nev=szemely.listanezet(), ceg=szervezet.listanezet())