from csomo import Csomo
from projekt import Projekt
from munkaresz import Munkaresz
from cim import Cim


class Jelleg(Csomo):
    "Munkarész jellegének megvalósítása. Egyszerű csomó, egy külső kulcsra támaszkodik."
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
        self._projekt_kon = None
    
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
    
    @property
    def projekt_kon(self):
        return self._projekt_kon
    
    @projekt_kon.setter
    def projekt_kon(self, kon):
        self._projekt_kon = kon
    
    def listanezet(self):
        """Egy adott azonosítójú jelleghez egy munkarész, így egy projekt tartozik."""
        if self._projekt_kon:
            munkaresz = self._projekt_kon.select("munkaresz", azonosito=self.munkaresz).fetchone()
            munkaresz = Munkaresz(**munkaresz)
            cim = self._projekt_kon.select("cim", munkaresz=munkaresz.azonosito).fetchone()
            cim = Cim(**cim)
            projekt = self._projekt_kon.select("projekt", azonosito=munkaresz.projekt).fetchone()
            projekt = Projekt(**projekt)
            return "{projekt}, {hely}, {munkaresz}, {jelleg}".format(projekt=str(projekt),
                                                                     hely=cim.helyseg,
                                                                     munkaresz=str(munkaresz),
                                                                     jelleg=str(self))
        else:
            raise NotImplementedError