from .alapcsomo import Csomo
from .munkaresz import Munkaresz


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
        return "{}{}".format(self.listanezet(), self._nullazo(self.megjegyzes))
    
    def __repr__(self):
        return "{}{}".format(repr(self._munkaresz()), self._ascii_rep(self.megnevezes))

    def __bool__(self):
        return bool(self.megnevezes)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, jelleg):
        self._adatok["megnevezes"] = jelleg.megnevezes
        self._adatok["megjegyzes"] = jelleg.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def munkaresz(self):
        return self._adatok.get("munkaresz")

    @munkaresz.setter
    def munkaresz(self, munkaresz):
        self._adatok["munkaresz"] = munkaresz
    
    def _munkaresz(self) -> Munkaresz:
        """Munkarész adatai."""
        assert self._kon
        munkaresz = self._kon.projekt.select("munkaresz", azonosito=self.munkaresz).fetchone()
        return Munkaresz(kon=self._kon, **munkaresz)

    
    def listanezet(self) -> str:
        """Egy adott azonosítójú jelleghez egy munkarész, így egy projekt tartozik."""
        return "{}, {}".format(self._munkaresz().listanezet(), self.megnevezes)