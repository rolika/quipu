from szervezet import Szervezet
from vevo import Vevo


class Szallito(Vevo):
    """Szállítók megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(**kwargs)
        self._tabla = "szallito"

    def _szervezet(self) -> Szervezet:
        assert self._kon
        szervezet = self._kon.szervezet.select("szervezet", azonosito=self._kontakt().szervezet).fetchone()
        return Szervezet(**szervezet)

    def listanezet(self) -> str:
        return self._szervezet().listanezet()
