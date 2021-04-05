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
                "ajanlatiar": "",
                "leadva": "",
                "ervenyes": "",
                "esely": "",
                "megjegyzes": ""
            }
        self._tabla = "ajanlat"

    def __bool__(self):
        return True

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, ajanlat):
        self._adatok["ajanlatkeres"] = ajanlat.ajanlatkeres
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