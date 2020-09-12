import dolog
import szemely
import szervezet


class Kontakt(dolog.Dolog):
    """Kontaktszemély megvalósítása"""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "szemely": 0,
                "szervezet": 0,
                "beosztas": "",
                "megjegyzes": ""
            }
        self._tabla = "kontakt"
    
    def __repr__(self):
        return "Roli"
    
    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")

    @property
    def beosztas(self):
        return self._adatok.get("beosztas")
    