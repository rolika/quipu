from csomo import Csomo
from jelleg import Jelleg
from kontakt import Kontakt
import copy


class Ajanlatkeres(Csomo):
    """
    Munkarész jellegének megvalósítása. Összetett csomó, több külső kulcsra támaszkodik.
    jelleg:         a projektet a jellegénél fogva tudjuk megjeleníteni (SQL PRIMARY KEY)
    ajánlatkérő:    a kontaktszemély, aki kéri az ajánlatot (SQL PRIMARY KEY)
    témafelelős:    a cégünk alkalmazottja, aki készíti az ajánlatot (SQL PRIMARY KEY)
    érkezett:       az ajánlatkérés beérkezési dátuma (ISO-formátum: éééé-hh-nn)
    határidő:       az ajánlat leadásának határideje (ISO-formátum: éééé-hh-nn)
    megjegyzés:     az ajánlatkéréshez fűzött megjegyzés (szöveg)
    """
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "jelleg": 0,
                "ajanlatkero": 0,
                "temafelelos": "",
                "erkezett": "",
                "hatarido": "",
                "megjegyzes": ""
            }
        self._tabla = "ajanlatkeres"
    
    def __str__(self):
        return self.listanezet()
    
    def __repr__(self):
        return self._ascii_rep(self.listanezet())

    def __bool__(self):
        return True

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, ajanlatkeres):
        self._adatok["jelleg"] = ajanlatkeres.jelleg
        self._adatok["ajanlatkero"] = ajanlatkeres.ajanlatkero
        self._adatok["temafelelos"] = ajanlatkeres.temafelelos
        self._adatok["erkezett"] = ajanlatkeres.erkezett
        self._adatok["hatarido"] = ajanlatkeres.hatarido
        self._adatok["megjegyzes"] = ajanlatkeres.megjegyzes

    @property
    def jelleg(self):
        return self._adatok.get("jelleg")

    @property
    def ajanlatkero(self):
        return self._adatok.get("ajanlatkero")

    @property
    def temafelelos(self):
        return self._adatok.get("temafelelos")

    @property
    def erkezett(self):
        return self._adatok.get("erkezett")

    @property
    def hatarido(self):
        return self._adatok.get("hatarido")
    
    def listanezet(self):
        if self._szemely_kon and self._szervezet_kon and self._kontakt_kon and self._projekt_kon:
            jelleg = self._projekt_kon.select("jelleg", azonosito=self.jelleg).fetchone()
            jelleg = Jelleg(**jelleg)
            jelleg.projekt_kon = self._projekt_kon
            kontakt = self._kontakt_kon.select("kontakt", azonosito=self.ajanlatkero).fetchone()
            kontakt = Kontakt(**kontakt)
            kontakt.szemely_kon = self._szemely_kon
            kontakt.szervezet_kon = self._szervezet_kon
            return "{jelleg} / {ajanlatkero}".format(jelleg=jelleg.listanezet(),
                                                     ajanlatkero=kontakt.listanezet())
        else:
            raise NotImplementedError