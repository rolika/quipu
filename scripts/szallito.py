from vevo import Vevo


class Szallito(Vevo):
    """Szállítók megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(**kwargs)
        self._tabla = "szallito"