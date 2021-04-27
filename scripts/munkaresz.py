from csomo import Csomo
from projekt import Projekt
from cim import Cim


class Munkaresz(Csomo):
    """Munkarész megvalósítása. Egyszerű csomó, egy külső kulcsra támaszkodik."""
    def __init__(self, **kwargs):
        super().__init__(kwargs.pop("kon", None))
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

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, uj):
        self._adatok["megnevezes"] = uj.megnevezes
        self._adatok["enaplo"] = uj.enaplo
        self._adatok["megjegyzes"] = uj.megjegyzes

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

    def listanezet(self):
        assert self._kon
        projekt = self._kon.projekt.select("projekt", azonosito=self.projekt).fetchone()
        projekt = Projekt(**projekt)
        cim = self._kon.projekt.select("cim", munkaresz=self.azonosito).fetchone()
        cim = Cim(**cim)
        return "{}, {}, {}".format(projekt.listanezet(), cim.helyseg, self.megnevezes)