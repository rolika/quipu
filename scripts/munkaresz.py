from dolog import Dolog


class Munkaresz(Dolog):
    """Munkarész megvalósítása"""
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "enaplo": 0,
                "megjegyzes": ""
            }
        self._tabla = "munkaresz"

    def __str__(self):
        return "{}{}".format(self.megnevezes, self._nullazo(self.megjegyzes))

    def __repr__(self):
        return self._ascii_rep("{}{}".format(self.megnevezes, self._nullazo(self.megjegyzes)))

    def __bool__(self):
        return bool(self.megnevezes)

    def listanezet(self):
        return str(self)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, projekt):
        self._adatok["megnevezes"] = projekt.megnevezes
        self._adatok["enaplo"] = projekt.cim
        self._adatok["megjegyzes"] = projekt.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def enaplo(self):
        return self._adatok.get("enaplo")

    @property
    def projekt(self):
        return self._adatok.get("projekt")

    @projekt.setter
    def projekt(self, projekt):
        self._adatok["projekt"] = projekt