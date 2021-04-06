from ajanlatkeres import Ajanlatkeres
from csomo import Csomo
from jelleg import Jelleg
from kontakt import Kontakt
from projekt import Projekt
from munkaresz import Munkaresz
from cim import Cim


class Ajanlat(Csomo):
    """
    Ajánlat megvalósítása. Egyszerű csomó, egy külső kulcsra támaszkodik.
    ajánlatkérés:   az ajánlat erre a kérésre készül (SQL PRIMARY KEY)
    ajánlati ár:    az ajánlati ár (nettó, forint)
    leadva:         az ajánlat ekkor került leadásra (ISO-formátum: éééé-hh-nn)
    érvényes:       az ajánlat árai eddig érvényesek (ISO-formátum: éééé-hh-nn)
    esély:          nyerési esélyünk %-ban (egész szám)
    megjegyzés:     az ajánlathoz fűzött megjegyzés (szöveg)
    """
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "ajanlatkeres": 0,
                "ajanlatiar": "",
                "leadva": "",
                "ervenyes": "",
                "esely": "",
                "megjegyzes": ""
            }
        self._tabla = "ajanlat"
        self._projekt_kon = None
        self._kontakt_kon = None
        self._szervezet_kon = None
        self._szemely_kon = None

    def __bool__(self):
        return True

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, ajanlat):
        self._adatok["ajanlatiar"] = ajanlat.ajanlatiar
        self._adatok["leadva"] = ajanlat.leadva
        self._adatok["ervenyes"] = ajanlat.ervenyes
        self._adatok["esely"] = ajanlat.esely
        self._adatok["megjegyzes"] = ajanlat.megjegyzes

    @property
    def ajanlatkeres(self):
        return self._adatok.get("ajanlatkeres")
    
    @ajanlatkeres.setter
    def ajanlatkeres(self, ajker):
        self._adatok["ajanlatkeres"] = ajker

    @property
    def ajanlatiar(self):
        return self._adatok.get("ajanlatiar", "")

    @property
    def leadva(self):
        return self._adatok.get("leadva", "")

    @property
    def ervenyes(self):
        return self._adatok.get("ervenyes", "")

    @property
    def esely(self):
        return self._adatok.get("esely", "")
    
    @property
    def projekt_kon(self):
        return self._projekt_kon
    
    @projekt_kon.setter
    def projekt_kon(self, kon):
        self._projekt_kon = kon
    
    @property
    def kontakt_kon(self):
        return self._kontakt_kon
    
    @projekt_kon.setter
    def kontakt_kon(self, kon):
        self._kontakt_kon = kon
    
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
        if self._szemely_kon and self._szervezet_kon and self._kontakt_kon and self._projekt_kon:
            ajanlatkeres = self._ajanlat_kon("ajanlatkeres", azonosito=self.ajanlatkeres).fetchone()
            ajanlatkeres = Ajanlatkeres(**ajanlatkeres)
            ajanlatkeres.projekt_kon = self._projekt_kon
            ajanlatkeres.kontakt_kon = self._kontakt_kon
            ajanlatkeres.szemely_kon = self._szemely_kon
            ajanlatkeres.szervezet_kon = self._szervezet_kon
            return "{ajanlatkeres}: {ar}".format(ajanlatkeres=ajanlatkeres.listanezet(), ar=self.ajanlatiar)
        else:
            raise NotImplementedError
    
