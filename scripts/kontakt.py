import dolog
import szemely
import szervezet


class Kontakt(dolog.Dolog):
    """Kontaktszemély megvalósítása"""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        self._adatok = dict(kwargs)  # itt nincs csak konkrét adatokkal példányosítás
        self._tabla = "kontakt"
    
    def __repr__(self):
        return "Roli"
    
    @property
    def szemely(self):
        return None
    