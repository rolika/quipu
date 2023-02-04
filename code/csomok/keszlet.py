from .alapcsomo import Csomo
from .termek import Termek


class Keszlet(Csomo):
    """A készlet tartalmazza egy adott termék raktári mennyiségét."""
    def __init__(self, **kwargs) -> object:
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {  # űrlap alaphelyzetbe állítására
                "mennyiseg": 0.0,
                "hely": "",
                "erkezett": "",
                "megjegyzes": ""
            }
        self._tabla = "keszlet"
    
    def __str__(self) -> str:
        return self.listanezet()
    
    def __repr__(self) -> str:
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self) -> bool:
        """A készlet akkor meghatározott, ha van mennyisége."""
        return bool(self.mennyiseg)

    @property
    def adatok(self) -> dict:
        return self._adatok

    @adatok.setter
    def adatok(self, keszlet) -> None:
        self._adatok["termek"] = keszlet.termek
        self._adatok["mennyiseg"] = keszlet.mennyiseg
        self._adatok["hely"] = keszlet.hely,
        self._adatok["erkezett"] = keszlet.erkezett
        self._adatok["megjegyzes"] = keszlet.megjegyzes
    
    @property
    def termek(self) -> Termek:
        return  self._adatok["termek"]
    
    @property
    def mennyiseg(self) -> float:
        return self._adatok["mennyiseg"]
    
    @mennyiseg.setter
    def mennyiseg(self, mennyiseg) -> None:
        self._adatok["mennyiseg"] = mennyiseg
    
    @property
    def hely(self) -> str:
        return self._adatok["hely"]

    @hely.setter
    def hely(self, hely) -> None:
        self._adatok["hely"] = hely
    
    @property
    def erkezett(self) -> str:
        return self._adatok["erkezett"]
    
    @erkezett.setter
    def erkezett(self, erkezett) -> None:
        self._adatok["erkezett"] = erkezett
    
    def listanezet(self) -> str:
        assert self._kon
        return "{termek}: {mennyiseg}".format(termek=Termek.adatbazisbol(self._kon, self.termek).listanezet(), mennyiseg=self.mennyiseg)

    