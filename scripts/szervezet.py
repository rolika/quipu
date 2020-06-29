import copy


class Szervezet:
    """Szervezet megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {
                "rovidnev": "",
                "teljesnev": "",
                "gyakorisag": 0,
                "vevo": 0,
                "szallito": 0,
                "megjegyzes": ""
            }

    def __str__(self):
        """Szervezeti adatok megjelenítése, elsősorban debugoláshoz"""
        megjegyzes = self._nullazo(self.megjegyzes)
        return "{}{}".format(self.rovidnev, megjegyzes)

    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.listanezet())

    def __bool__(self):
        """Egy szervezet akkor meghatározott, ha legalább a rövid neve adott"""
        return bool(self.rovidnev)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, uj):
        """Új szervezet-osztály alapján módosítja a meglévőt."""
        self._adatok["rovidnev"] = uj.rovidnev
        self._adatok["teljesnev"] = uj.teljesnev
        self._adatok["gyakorisag"] = uj.gyakorisag
        self._adatok["vevo"] = uj.vevo
        self._adatok["szallito"] = uj.szallito
        self._adatok["megjegyzes"] = uj.megjegyzes

    @property
    def azonosito(self):
        return self._adatok.get("azonosito")

    @property
    def rovidnev(self):
        return self._adatok.get("rovidnev")

    @property
    def teljesnev(self):
        return self._adatok.get("teljesnev")

    @property
    def vevo(self):
        return self._adatok.get("vevo")

    @property
    def szallito(self):
        return self._adatok.get("szallito")
    
    @property
    def gyakorisag(self):
        return self._adatok.get("gyakorisag")
    
    @property
    def vevo(self):
        return self._adatok.get("vevo")
    
    @property
    def szallito(self):
        return self._adatok.get("szallito")

    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes")

    def listanezet(self):
        """Szervezet megjelenítése kiválasztáshoz (Combobox)"""
        return str(self)

    def ment(self, kon):
        """Menti vagy módosítja a szervezeti adatokat"""
        if self.azonosito:
            return kon.update("szervezet", self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert("szervezet", **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból az szervezet-bejegyzést"""
        return kon.delete("szervezet", azonosito=self.azonosito)

    def meglevo(self, kon):
        """Ellenőrzi, hogy a szervezet szerepel-e az adatbázisban"""
        adatok = copy.copy(self._adatok)  # shallow copy
        adatok.pop("azonosito", None)
        return kon.select("szervezet", logic="AND", **adatok).fetchone()

    def _ascii_rep(self, szoveg):
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))

    def _nullazo(self, attr):
        """Ha hiányzik az adat, nem írjuk ki egyáltalán."""
        return ", {}".format(attr) if attr else ""


if __name__ == "__main__":
    """Egyszerű tesztelés"""
    pass