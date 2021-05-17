from csomo import Csomo
from szervezet import Szervezet
from termek import Termek


class Aru(Csomo):
    """Áru, azaz árral rendelkező termék megvalósítása."""
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
        """Az áru akkor meghatározott, ha van egységára."""
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
    def termek(self):
        return self._adatok["termek"]
    
    @termek.setter
    def termek(self, termek):
        self._adatok["termek"] = termek
    
    @property
    def forgalmazo(self):
        return self._adatok["forgalmazo"]
    
    @forgalmazo.setter
    def forgalmazo(self, szervezet):
        self._adatok["forgalmazo"] = szervezet
    
    def _termek(self) -> Termek:
        assert self._kon
        termek = self._kon.raktar.select("termek", azonosito=self.termek).fetchone()
        return Termek(kon=self._kon, **termek)

    def _forgalmazo(self) -> Szervezet:
        assert self._kon
        forgalmazo = self._kon.szervezet.select("szervezet", azonosito=self.forgalmazo).fetchone()
        return Szervezet(kon=self._kon, **forgalmazo)
    
    def listanezet(self) -> str:
        return "{termek}: {ar}".format(termek=self._termek().listanezet(), ar=self.egysegar)
