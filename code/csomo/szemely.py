from .csomo import Csomo


class Szemely(Csomo):
    """Személy megvalósítása"""
    def __init__(self, **kwargs) -> Csomo:
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        sqlite Row-objektum is lehet (hozzáférés oszlopnevekkel)
        kwargs:
            elotag:     név előtagja, pl.: dr. mr. id. ifj.
            vezeteknev: vezetéknév
            keresztnev: keresztnév
            becenev:    becenév vagy rövidítés
            nem:        férfi vagy nő
            megjegyzes: bármilyen megjegyzés. Használható két, egyébként azonos
                        bejegyzés megkülönböztetésére"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {
                "elotag": "",
                "vezeteknev": "",
                "keresztnev": "",
                "becenev": "",
                "nem": "férfi",
                "megjegyzes": ""
            }
        self._db = "kontakt"
        self._tabla = "szemely"

    def __str__(self):
        """Személyi adatok megjelenítése terminál-nézethez."""
        return "{vezeteknev} {keresztnev}{elotag} ({nem}{megjegyzes})".format(\
            vezeteknev=self.vezeteknev,
            keresztnev=self.keresztnev,
            elotag=Csomo.formazo(self.elotag, zarojel="", elvalasztojel=", "),
            nem=self.nem,
            megjegyzes=Csomo.formazo(self.megjegyzes,
                                     zarojel="",
                                     elvalasztojel=", "))

    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return Csomo.ascii_rep("{vezetek} {kereszt}".\
            format(vezetek=self.vezeteknev, kereszt=self.keresztnev))

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
        self._adatok["becenev"] = uj.becenev
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
    def becenev(self):
        return self._adatok.get("becenev", "")

    @property
    def nem(self):
        return self._adatok.get("nem")

    def listanezet(self) -> str:
        """Személy megjelenítése kiválasztáshoz (Combobox)"""
        return "{elotag}{vezeteknev} {keresztnev}".\
            format(elotag=Csomo.formazo(self.elotag,
                   zarojel="",
                   hatul=True),
                   vezeteknev=self.vezeteknev,
                   keresztnev=self.keresztnev)

    def megszolitas(self):
        return "Tisztelt {}!".format("Uram" if self.nem == "férfi" else "Hölgyem")
