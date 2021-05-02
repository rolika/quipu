from csomo import Csomo


class Szervezet(Csomo):
    """Szervezet megvalósítása. Alapvető csomó, nem támaszkodik külső kulcsra."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {
                "rovidnev": "",
                "teljesnev": "",
                "gyakorisag": 0,
                "megjegyzes": ""
            }
        self._tabla = "szervezet"

    def __str__(self) -> str:
        """Szervezeti adatok megjelenítése terminál-nézethez."""
        return "{nev}{meg}".format(nev=self.teljesnev or self.rovidnev, meg=self._nullazo(self.megjegyzes))

    def __repr__(self) -> str:
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.teljesnev or self.rovidnev)

    def __bool__(self) -> bool:
        """Egy szervezet akkor meghatározott, ha legalább a rövid neve adott"""
        return bool(self.rovidnev)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, uj):
        """Új szervezet-osztály alapján módosítja a meglévőt.
        uj: Szervezet() objektum"""
        self._adatok["rovidnev"] = uj.rovidnev
        self._adatok["teljesnev"] = uj.teljesnev
        self._adatok["gyakorisag"] = uj.gyakorisag
        self._adatok["megjegyzes"] = uj.megjegyzes

    @property
    def rovidnev(self):
        return self._adatok.get("rovidnev")
    
    @rovidnev.setter
    def rovidnev(self, nev):
        self._adatok["rovidnev"] = nev

    @property
    def teljesnev(self):
        return self._adatok.get("teljesnev")

    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")

    def listanezet(self) -> str:
        """Szervezet megjelenítése kiválasztáshoz (Combobox)"""
        return self.rovidnev


if __name__ == "__main__":
    """Egyszerű tesztelés"""
    wevik = Szervezet(rovidnev="Wevik")
    print(wevik)
    pohlen = Szervezet(rovidnev="Pohlen-Dach", teljesnev="Pohlen-Dach Hungária Bt.", megjegyzes="nagy cég")
    print(pohlen)
