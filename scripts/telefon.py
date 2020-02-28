class Telefon(dict):
    """Telefonos elérhetőség megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "telefonszam": "",
                "megjegyzes": ""
            }

    def __bool__(self):
        """Telefonszámot kötelező megadni."""
        return bool(self.telefonszam)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, telefon):
        """Új telefon-osztály alapján módosítja a meglévőt."""
        self._adatok["telefonszam"] = telefon.telefonszam
        self._adatok["megjegyzes"] = telefon.megjegyzes

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
    def telefonszam(self):
        return self._adatok.get("telefonszam")

    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes")

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{} ({})".format(self.telefonszam, self.megjegyzes)

    def ment(self, kon):
        """Menti vagy módosítja az telefon-adatokat"""
        if self.azonosito:
            return kon.update("telefon", self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert("telefon", **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból az telefon-bejegyzést"""
        return kon.delete("telefon", azonosito=self.azonosito)
