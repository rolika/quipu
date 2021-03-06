import dolog


class Ajanlatkeres(dolog.Dolog):
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "munkaresz": 0,
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
        self._adatok["munkaresz"] = ajanlatkeres.munkaresz
        self._adatok["ajanlatkero"] = ajanlatkeres.ajanlatkero
        self._adatok["temafelelos"] = ajanlatkeres.temafelelos
        self._adatok["erkezett"] = ajanlatkeres.erkezett
        self._adatok["hatarido"] = ajanlatkeres.hatarido
        self._adatok["megjegyzes"] = ajanlatkeres.megjegyzes

    @property
    def munkaresz(self):
        return self._adatok.get("munkaresz")

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