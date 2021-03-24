from csomo import Csomo


class Projekt(Csomo):
    """Projekt megvalósítása. Alapvető csomó."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "megnevezes": "",
                "rovidnev": "",
                "ev": 0,
                "szam": 0,
                "gyakorisag": 0,
                "megjegyzes": ""
            }
        self._tabla = "projekt"

    def __str__(self):
        """Projekt kiíratása emberi használatra"""
        return "{}/{} {}{}".format(self.ev, self.szam, self.megnevezes, self._nullazo(self.megjegyzes))

    def __repr__(self):
        """Projekt elnevezése sorbarendezéshez"""
        return "{}{}{}{}".format(self.ev, self.szam, self._ascii_rep(self.megnevezes), self._ascii_rep(self.megjegyzes))

    def __bool__(self):
        """ A projekt meghatározott, ha adott a megnevezése."""
        return bool(self.megnevezes)

    def listanezet(self):
        return str(self)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, uj):
        self._adatok["megnevezes"] = uj.megnevezes
        self._adatok["rovidnev"] = uj.rovidnev
        self._adatok["megjegyzes"] = uj.megjegyzes

    @property
    def megnevezes(self):
        return self._adatok.get("megnevezes")

    @property
    def rovidnev(self):
        return self._adatok.get("rovidnev")

    @property
    def ev(self):
        return self._adatok.get("ev")

    @ev.setter
    def ev(self, evszam):
        self._adatok["ev"] = evszam

    @property
    def szam(self):
        return self._adatok.get("szam")

    @szam.setter
    def szam(self, projektszam):
        self._adatok["szam"] = projektszam

    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")

    @gyakorisag.setter
    def gyakorisag(self, ertek):
        self._adatok["gyakorisag"] = ertek

    def hozzafer(self):
        self._adatok["gyakorisag"] -= 1


