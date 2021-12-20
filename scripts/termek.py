from csomo import Csomo
from szallito import Szallito
from anyag import Anyag


class Termek(Csomo):
    """Termék, azaz árral rendelkező anyag megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {  # űrlap alaphelyzetbe állítására
                "egysegar": 0,
                "ervenyes": "",
                "megjegyzes": ""
            }
    
    def __str__(self) -> str:
        return self.listanezet()
    
    def __repr__(self) -> str:
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self) -> bool:
        """A termék akkor meghatározott, ha van egységára."""
        return bool(self.egysegar)

    @property
    def adatok(self) -> dict:
        return self._adatok

    @adatok.setter
    def adatok(self, aru) -> None:
        self._adatok["egysegar"] = aru.egysegar
        self._adatok["ervenyes"] = aru.ervenyes
        self._adatok["megjegyzes"] = aru.megjegyzes
    
    @property
    def anyag(self):
        return self._adatok["anyag"]
    
    @anyag.setter
    def anyag(self, anyag):
        self._adatok["anyag"] = anyag
    
    @property
    def szallito(self):
        return self._adatok["szallito"]
    
    @szallito.setter
    def szallito(self, szallito):
        self._adatok["szallito"] = szallito
    
    def _anyag(self) -> Anyag:
        assert self._kon
        anyag = self._kon.raktar.select("anyag", azonosito=self.anyag).fetchone()
        return Anyag(kon=self._kon, **anyag)

    def _szallito(self) -> Szallito:
        assert self._kon
        szallito = self._kon.kontakt.select("szallito", azonosito=self.szallito).fetchone()
        return Szallito(kon=self._kon, **szallito)
    
    def listanezet(self) -> str:
        return "{termek}: {ar}".format(termek=self._termek().listanezet(), ar=self.egysegar)
