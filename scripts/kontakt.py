from csomo import Csomo
from szemely import Szemely
from szervezet import Szervezet
from konstans import MAGANSZEMELY


class Kontakt(Csomo):
    """Kontaktszemély megvalósítása. Összetett csomó, több külső kulcsra támaszkodik."""
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
                "megjegyzes": ""
            }
        self._tabla = "kontakt"
        self._szemely_kon = None
        self._szervezet_kon = None
    
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
    
    @property
    def szervezet_kon(self):
        return self._szervezet_kon
    
    @szervezet_kon.setter
    def szervezet_kon(self, kon):
        self._szervezet_kon = kon
    
    @property
    def szemely_kon(self):
        return self._szemely_kon
    
    @szemely_kon.setter
    def szemely_kon(self, kon):
        self._szemely_kon = kon
    
    def listanezet(self):
        if self._szemely_kon and self._szervezet_kon:
            szemely = self._szemely_kon.select("szemely", azonosito=self.szemely).fetchone()
            szemely = Szemely(**szemely)
            szervezet = self._szervezet_kon.select("szervezet", azonosito=self.szervezet).fetchone()
            szervezet = Szervezet(**szervezet)
            if szervezet.azonosito == MAGANSZEMELY.azonosito:
                szervezet.rovidnev = ""
            return "{nev}{ceg}".format(nev=szemely.listanezet(), 
                                       ceg=self._nullazo(str(szervezet), zarojel="", elvalasztojel="/"))
        else:
            raise NotImplementedError