from code.csomok.alapcsomo import Csomo
from code.csomok.kontakt import Kontakt


class Vevo(Csomo):
    """Vevő megvalósítása."""
    def __init__(self, **kwargs) -> object:
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        sqlite Row-objektum is lehet (hozzáférés oszlopnevekkel)
        kwargs:
            kontakt:    sql primery key"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "kontakt": 0
            }
        self._tabla = "vevo"
    
    def __str__(self) -> str:
        return str(self._kontakt())
    
    def __repr__(self) -> str:
        return repr(self._kontakt())
    
    def __bool__(self) -> bool:
        return True
    
    @property
    def kontakt(self):
        return self._adatok.get("kontakt")
    
    def _kontakt(self) -> Kontakt:
        """Kontaktszemély előhívása."""
        kontakt = self._kon.kontakt.\
            select("kontakt", azonosito=self.kontakt).fetchone()
        return Kontakt(kon=self._kon, **kontakt)
    
    def listanezet(self) -> str:
        return self._kontakt().listanezet()