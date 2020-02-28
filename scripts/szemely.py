class Szemely:
    """Személy megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        self._adatok = dict(kwargs)
        self._kon = None
    
    def __str__(self):
        """Személyi adatok megjelenítése, elsősorban debugoláshoz"""
        elotag = self._nullazo(self.elotag)
        megjegyzes = self._nullazo(self.megjegyzes)
        return "{}{} {}, {}{}".format(elotag, self.vezeteknev, self.keresztnev, self.nem, megjegyzes)
    
    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self):
        """Egy személy akkor meghatározott, ha legalább az egyik név adott"""
        return bool(self.vezeteknev) or bool(self.keresztnev)
    
    @property
    def adatok(self):
        return self._adatok
    
    @property
    def azonosito(self):
        return self._adatok.get("azonosito")
    
    @property
    def elotag(self):
        return self._adatok.get("elotag")
    
    @property
    def vezeteknev(self):
        return self._adatok.get("vezeteknev")
    
    @property
    def keresztnev(self):
        return self._adatok.get("keresztnev")
    
    @property
    def nem(self):
        return self._adatok.get("nem")
    
    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes")

    @property
    def kon(self):
        return self._kon

    @kon.setter
    def kon(self, kon_):
        self._kon = kon_
    
    def listanezet(self):
        """Személy megjelenítése kiválasztáshoz (Combobox)"""
        megjegyzes = self._nullazo(self.megjegyzes)
        return "{} {} {}{}".format(self.vezeteknev, self.keresztnev, self.elotag, megjegyzes)
    
    def modosit(self, szemely):
        """Új személy-osztály alapján módosítja a meglévőt."""
        self._adatok["elotag"] = szemely.elotag
        self._adatok["vezeteknev"] = szemely.vezeteknev
        self._adatok["keresztnev"] = szemely.keresztnev
        self._adatok["nem"] = szemely.nem
        self._adatok["megjegyzes"] = szemely.megjegyzes

    def ment(self):
        """Menti vagy módosítja a személyi adatokat"""
        if self.azonosito:
            return self._kon.update("szemely", self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return self._kon.insert("szemely", **self._adatok)  # lastrowid vagy None

    def torol(self):
        """Törli az adatbázisból az email-bejegyzést"""
        return self._kon.delete("szemely", azonosito=self.azonosito)
    
    def megszolitas(self):
        return "Tisztelt {}!".format("Uram" if self.nem == "férfi" else "Hölgyem")

    def _ascii_rep(self, szoveg):
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))
    
    def _nullazo(self, attr):
        """Ha hiányzik az adat, nem írjuk ki egyáltalán."""
        return ", {}".format(attr) if attr else ""


if __name__ == "__main__":
    """Egyszerű tesztelés"""
    import tamer
    szemely = Szemely(vezeteknev="Árvíztűrő", keresztnev="Tükörfúrógép")
    print(repr(szemely))  # arvizturo tukorfurogep
    szemely = Szemely(elotag="dr")
    if not szemely:
        print("Nincs elegendő adat")  # ki kell írnia
    szemely = Szemely(keresztnev="Roland")
    if szemely:
        print("Elegendő adat.")  # ki kell írnia
    kon = tamer.Tamer("szemely.db")
    szemely = Szemely.adatbazisbol(kon.select("szemely").fetchone())
    print(szemely)  # a lekérdezés első bejegyzését kell kiírnia
    print(szemely["vezeteknev"])  # lekérdezés első bejegyzésének vezetékneve
    print(szemely.azonosito)  # lekérdezés első bejegyzésének rowid-je