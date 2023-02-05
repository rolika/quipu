from code.csomok.szervezet import Szervezet
from code.csomok.vevo import Vevo


class Szallito(Vevo):
    """Szállítók megvalósítása."""
    def __init__(self, **kwargs) -> object:
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        sqlite Row-objektum is lehet (hozzáférés oszlopnevekkel)
        kwargs:
            kontakt:    sql primery key"""
        super().__init__(**kwargs)
        self._tabla = "szallito"

    def _szervezet(self) -> Szervezet:
        szervezet = self._kon.szervezet.\
            select("szervezet", azonosito=self._kontakt().szervezet).fetchone()
        return Szervezet(**szervezet)

    def listanezet(self) -> str:
        return self._szervezet().listanezet()
