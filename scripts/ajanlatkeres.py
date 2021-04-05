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
        self._projekt_kon = None
        self._kontakt_kon = None
        self._szervezet_kon = None
        self._szemely_kon = None
    
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

    def meglevo(self, kon):
        """Az ajánlatkérés meglévő, ha ugyanaz az ajánlatkérő és a jelleg"""
        adatok = copy.copy(self._adatok)  # shallow copy
        adatok.pop("azonosito", None)
        adatok.pop("erkezett", None)
        adatok.pop("hatarido", None)
        adatok.pop("temafelelos", None)
        return kon.select(self._tabla, logic="AND", **adatok).fetchone()
    
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