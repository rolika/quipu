from dolog import Dolog


class Jelleg(Dolog):
    "Munkarész jellegének megvalósítása"
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "megjegyzes": ""
            }
        self._tabla = "jelleg"

    def __bool__(self):
        return bool(self.megnevezes)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, projekt):
        self._adatok["megnevezes"] = projekt.megnevezes
        self._adatok["megjegyzes"] = projekt.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def munkaresz(self):
        return self._adatok.get("munkaresz")

    @munkaresz.setter
    def munkaresz(self, munkaresz):
        self._adatok["munkaresz"] = munkaresz