class Cim:
    """Cím megvalósítása"""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {oszlop: "" for oszlop in self.oszlopnevek}

    def __str__(self):
        return "{}-{} {}, {}".format(self.orszag, self.iranyitoszam, self.helyseg, self.utca)

    def __bool__(self):
        """Egy cím akkor meghatározott, ha legalább a helység adott"""
        return bool(self._adatok["helyseg"])

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, cim):
        """Új cím-osztály alapján módosítja a meglévőt."""
        for oszlop in self.oszlopnevek:
            self._adatok[oszlop] = getattr(cim, oszlop, "")

    @property
    def azonosito(self):
        return self._adatok.get("azonosito")

    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @szemely.setter
    def szemely(self, szemely):
        self._adatok["szemely"] = szemely

    @property
    def orszag(self):
        return self._adatok.get("orszag", "")

    @property
    def iranyitoszam(self):
        return self._adatok.get("iranyitoszam", "")

    @property
    def helyseg(self):
        return self._adatok.get("helyseg", "")

    @property
    def utca(self):
        return self._adatok.get("utca", "")

    @property
    def hrsz(self):
        return self._adatok.get("hrsz", "")

    @property
    def postafiok(self):
        return self._adatok.get("postafiok", "")

    @property
    def honlap(self):
        return self._adatok.get("honlap", "")

    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes", "")

    def listanezet(self):
        return str(self)

    def ment(self, kon):
        """Menti vagy módosítja a címadatokat"""
        if self.azonosito:
            return kon.update("cim", self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert("cim", **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból a cím-bejegyzést"""
        return kon.delete("cim", azonosito=self.azonosito)


if __name__ == "__main__":
    print(Cim().adatok)
