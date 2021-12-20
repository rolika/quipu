from vevo import Vevo


class Gyarto(Vevo):
    """Gyártók megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(**kwargs)
        self._tabla = "gyarto"