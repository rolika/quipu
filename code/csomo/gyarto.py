from .szervezet import Szervezet
from .vevo import Vevo


class Gyarto(Vevo):
    """Gyártók megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(**kwargs)
        self._tabla = "gyarto"
    
    def _szervezet(self) -> Szervezet:
        assert self._kon
        szervezet = self._kon.szervezet.select("szervezet", azonosito=self._kontakt().szervezet).fetchone()
        return Szervezet(**szervezet)
    
    def listanezet(self) -> str:
        return self._szervezet().listanezet()