from ajanlatkeres import Ajanlatkeres
from jelleg import Jelleg
from csomo import Csomo


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
                "ajanlatiar": 0,
                "leadva": "",
                "ervenyes": "",
                "esely": 5,
                "megjegyzes": ""
            }
        self._tabla = "ajanlat"

    def __bool__(self):
        """Az ajánlat akkor érvényes, ha 0-nál nagyobb egész számra konvertálható az ajánlati ár."""
        #try:
        assert int(self.ajanlatiar) > 0
        return True
        #except (ValueError, AssertionError):
        return False
    
    def __repr__(self):
        return self._ascii_rep(self.listanezet())

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
    
    @leadva.setter
    def leadva(self, datum):
        self._adatok["leadva"] = datum

    @property
    def ervenyes(self):
        return self._adatok.get("ervenyes", "")
    
    @ervenyes.setter
    def ervenyes(self, datum):
        self._adatok["ervenyes"] = datum

    @property
    def esely(self):
        return self._adatok.get("esely", "")
    
    @esely.setter
    def esely(self, uj):
        self._adatok["esely"] = uj
    
    def listanezet(self) -> str:
        if self._ajanlat_kon and self._projekt_kon:
            ajanlatkeres = self._ajanlat_kon.select("ajanlatkeres", azonosito=self.ajanlatkeres).fetchone()
            ajanlatkeres = Ajanlatkeres(**ajanlatkeres)
            jelleg = self._projekt_kon.select("jelleg", azonosito=ajanlatkeres.jelleg).fetchone()
            jelleg = Jelleg(**jelleg)
            jelleg.projekt_kon = self._projekt_kon
            return "{jelleg}: {ar}".format(jelleg=jelleg.listanezet(), ar=self.ajanlatiar)
        else:
            raise NotImplementedError
    
