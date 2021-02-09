from dolog import Dolog


class Projekt(Dolog):
    """Projekt megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "gyakorisag": 0,
                "megjegyzes": ""
            }
        self._tabla = "projekt"

    def __bool__(self):
        """ A projekt meghatározott, ha adott a megnevezése."""
        return bool(self.megnevezes)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, projekt):
        self._adatok["megnevezes"] = projekt.megnevezes
        self._adatok["gyakorisag"] = projekt.gyakorisag
        self._adatok["megjegyzes"] = projekt.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")

    def hozzanyul(self):
        self._adatok["gyakorisag"] += 1
