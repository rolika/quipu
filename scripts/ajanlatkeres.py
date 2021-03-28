from csomo import Csomo
import copy


class Ajanlatkeres(Csomo):
    "Munkarész jellegének megvalósítása. Összetett csomó, több külső kulcsra támaszkodik."
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

    def meglevo(self, kon):
        """Az ajánlatkérés meglévő, ha ugyanaz az ajánlatkérő és a jelleg"""
        adatok = copy.copy(self._adatok)  # shallow copy
        adatok.pop("azonosito", None)
        adatok.pop("erkezett", None)
        adatok.pop("hatarido", None)
        adatok.pop("temafelelos", None)
        return kon.select(self._tabla, logic="AND", **adatok).fetchone()