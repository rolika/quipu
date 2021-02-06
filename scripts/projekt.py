import dolog


class Projekt(dolog.Dolog):
    """Projekt megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
            self._adatok["gyakorisag"] = 0
        else:
            self._adatok ={
                "megnevezes": "",
                "gyakorisag": 0,
                "megjegyzes": ""
            }
        self._tabla = "projekt"

    def __bool__(self):
        """Egy projekt meghatározott, ha ismert legalább a neve és helye (helység)"""
        return bool(self.megnevezes) and bool(self.cim) and bool(self.munkaresz)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, projekt):
        self._adatok["megnevezes"] = projekt.megnevezes
        self._adatok["cim"] = projekt.cim
        self._adatok["munkaresz"] = projekt.munkaresz
        self._adatok["jelleg"] = projekt.jelleg
        self._adatok["gyakorisag"] = projekt.gyakorisag
        self._adatok["megjegyzes"] = projekt.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def cim(self):
        return self._adatok.get("cim")

    @property
    def munkaresz(self):
        return self._adatok.get("munkaresz")

    @property
    def jelleg(self):
        return self._adatok.get("jelleg")

    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")

    def gyakori(self):
        self._adatok["gyakorisag"] += 1

