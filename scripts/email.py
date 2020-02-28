class Email:
    """Email-elérhetőség megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        self._adatok = dict(kwargs)

    def __bool__(self):
        return bool(self.emailcim)
    
    @property
    def adatok(self):
        return self._adatok
    
    @adatok.setter
    def adatok(self, email):
        """Új email-osztály alapján módosítja a meglévőt."""
        self._adatok["emailcim"] = email.emailcim
        self._adatok["megjegyzes"] = email.megjegyzes

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
    def emailcim(self):
        return self._adatok.get("emailcim")

    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes")

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{} ({})".format(self.emailcim, self.megjegyzes)

    def ment(self, kon):
        """Menti vagy módosítja az emailcím-adatokat"""
        if self.azonosito:
            return kon.update("email", self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert("email", **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból az email-bejegyzést"""
        return kon.delete("email", azonosito=self.azonosito)

