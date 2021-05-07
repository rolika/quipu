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
        return "{projekt}{hely}{nev}".format(projekt=repr(self._projekt()),
                                             hely=self._ascii_rep(self._cim().helyseg),
                                             nev=self._ascii_rep(self.megnevezes))

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
    
    def _projekt(self) -> Projekt:
        """Projekt adatai."""
        assert self._kon
        projekt = self._kon.projekt.select("projekt", azonosito=self.projekt).fetchone()
        return Projekt(kon=self._kon, **projekt)
    
    def _cim(self) -> Cim:
        """Cím adatai."""
        cim = self._kon.projekt.select("cim", munkaresz=self.azonosito).fetchone()
        return Cim(**cim)

    def listanezet(self):
        return "{projekt}, {hely}, {nev}".format(projekt=self._projekt().listanezet(),
                                                 hely=self._cim().helyseg,
                                                 nev=self.megnevezes)