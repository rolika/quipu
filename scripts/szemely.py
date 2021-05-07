from csomo import Csomo


class Szemely(Csomo):
    """Személy megvalósítása. Alapvető csomó, nem támaszkodik külső kulcsra."""
    def __init__(self, **kwargs) -> Csomo:
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {
                "elotag": "",
                "vezeteknev": "",
                "keresztnev": "",
                "nem": "férfi",
                "megjegyzes": ""
            }
        self._tabla = "szemely"

    def __str__(self):
        """Személyi adatok megjelenítése terminál-nézethez."""
        return "{vezeteknev} {keresztnev}{elotag} ({nem}{megjegyzes})".format(\
            vezeteknev=self.vezeteknev,
            keresztnev=self.keresztnev,
            elotag=self._nullazo(self.elotag, zarojel="", elvalasztojel=", "),
            nem=self.nem,
            megjegyzes=self._nullazo(self.megjegyzes, zarojel="", elvalasztojel=", "))

    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep("{vezetek} {kereszt}".format(vezetek=self.vezeteknev, kereszt=self.keresztnev))

    def __bool__(self):
        """Egy személy akkor meghatározott, ha legalább az egyik név adott"""
        return bool(self.vezeteknev) or bool(self.keresztnev)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, uj):
        """Új személy-osztály alapján módosítja a meglévőt.
        uj: Szemely() objektum"""
        self._adatok["elotag"] = uj.elotag
        self._adatok["vezeteknev"] = uj.vezeteknev
        self._adatok["keresztnev"] = uj.keresztnev
        self._adatok["nem"] = uj.nem
        self._adatok["megjegyzes"] = uj.megjegyzes

    @property
    def elotag(self):
        return self._adatok.get("elotag")

    @property
    def vezeteknev(self):
        return self._adatok.get("vezeteknev", "")

    @property
    def keresztnev(self):
        return self._adatok.get("keresztnev", "")

    @property
    def nem(self):
        return self._adatok.get("nem")

    def listanezet(self) -> str:
        """Személy megjelenítése kiválasztáshoz (Combobox)"""
        return "{elotag}{vezeteknev} {keresztnev}".format(elotag=self._nullazo(self.elotag, zarojel="", hatul=True),
                                                          vezeteknev=self.vezeteknev,
                                                          keresztnev=self.keresztnev)

    def megszolitas(self):
        return "Tisztelt {}!".format("Uram" if self.nem == "férfi" else "Hölgyem")


if __name__ == "__main__":
    """Egyszerű tesztelés"""
    szemely = Szemely(vezeteknev="Árvíz-tűrő", keresztnev="Tükör+fúrógép", elotag="Mr.", nem="SDS", megjegyzes="Max")
    print(repr(szemely))  # arvizturotukorfurogep
    print(szemely)
    print(szemely.listanezet())
    szemely = Szemely(elotag="dr")
    if not szemely:
        print("Nincs elegendő adat")  # ki kell írnia
    szemely = Szemely(keresztnev="Roland")
    if szemely:
        print("Elegendő adat.")  # ki kell írnia
