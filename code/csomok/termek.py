from .alapcsomo import Csomo
from .szallito import Szallito
from .anyag import Anyag


class Termek(Csomo):
    """Termék, azaz árral rendelkező anyag megvalósítása."""
    tabla = "termek"

    def __init__(self, **kwargs) -> object:
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {  # űrlap alaphelyzetbe állítására
                "egysegar": 0,
                "megjegyzes": ""
            }
        self._tabla = Termek.tabla
    
    def __str__(self) -> str:
        return self.listanezet()
    
    def __repr__(self) -> str:
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self) -> bool:
        """A termék akkor meghatározott, ha van egységára."""
        return bool(self.egysegar)
    
    @classmethod
    def adatbazisbol(cls, kon, azonosito):
        termek = kon.raktar.select(cls.tabla, azonosito=azonosito).fetchone()
        return cls(kon=kon, **termek)

    @property
    def adatok(self) -> dict:
        return self._adatok

    @adatok.setter
    def adatok(self, termek) -> None:
        self._adatok["anyag"] = termek.anyag
        self._adatok["szallito"] = termek.szallito
        self._adatok["egysegar"] = termek.egysegar
        self._adatok["megjegyzes"] = termek.megjegyzes
    
    @property
    def anyag(self):
        return self._adatok["anyag"]
    
    @property
    def szallito(self):
        return self._adatok["szallito"]
    
    @property
    def egysegar(self):
        return self._adatok["egysegar"]

    @property
    def szallito_teljes(self) -> Szallito:
        assert self._kon
        szallito = self._kon.kontakt.select("szallito", azonosito=self.szallito).fetchone()
        return Szallito(kon=self._kon, **szallito)
    
    def listanezet(self) -> str:
        assert self._kon
        return "{anyag}: {ar}".format(anyag=Anyag.adatbazisbol(self._kon, self.anyag).listanezet(), ar=self.egysegar)
