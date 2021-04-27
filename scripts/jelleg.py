from csomo import Csomo
from munkaresz import Munkaresz


class Jelleg(Csomo):
    "Munkarész jellegének megvalósítása. Egyszerű csomó, egy külső kulcsra támaszkodik."
    def __init__(self, **kwargs):
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "megjegyzes": ""
            }
        self._tabla = "jelleg"
    
    def __str__(self):
        return "{}{}".format(self.megnevezes, self._nullazo(self.megjegyzes))
    
    def __repr__(self):
        return self._ascii_rep(self.listanezet())

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
    
    def listanezet(self) -> str:
        """Egy adott azonosítójú jelleghez egy munkarész, így egy projekt tartozik."""
        assert self._kon
        munkaresz = self._kon.projekt.select("munkaresz", azonosito=self.munkaresz).fetchone()
        munkaresz = Munkaresz(kon=self._kon, **munkaresz)
        return "{}, {}".format(munkaresz.listanezet(), self.megnevezes)