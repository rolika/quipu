class Szemely(dict):
    """ Személy megvalósítása kulcs-érték párokkal """
    def __init__(self, **kwargs):
        """Konstruktor közvetlen példányosításhoz:
        kwargs:     személyi adatok kulcs=érték párokként"""
        super().__init__(kwargs)
        self._db_oszlop = {"azonosito", "elotag", "vezeteknev", "keresztnev", "nem", "megjegyzes"}
        for oszlop in self._db_oszlop:
            self[oszlop] = kwargs.get(oszlop, "")
    
    def __str__(self):
        """Személyi adatok megjelenítése, elsősorban debugoláshoz"""
        elotag = self._nullazo(self["elotag"])
        megjegyzes = self._nullazo(self["megjegyzes"])
        return "{}{} {}, {}{}".format(elotag, self["vezeteknev"], self["keresztnev"], self["nem"], megjegyzes)
    
    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self):
        """Egy személy akkor meghatározott, ha legalább az egyik név adott"""
        return bool(self["vezeteknev"]) or bool(self["keresztnev"])

    @classmethod
    def adatbazisbol(cls, row):
        """Factory konstruktor adatbázisból történő példányososításhoz:
        kurzor:     sqlite Row-objektum (hozzáférés oszlopnevekkel)"""
        return cls(**row)
    
    @property
    def azonosito(self):
        """Kényelmi megoldás."""
        return self["azonosito"]
    
    @property
    def elotag(self):
        """Kényelmi megoldás."""
        return self["elotag"]
    
    @property
    def vezeteknev(self):
        """Kényelmi megoldás."""
        return self["vezeteknev"]
    
    @property
    def keresztnev(self):
        """Kényelmi megoldás."""
        return self["keresztnev"]
    
    @property
    def nem(self):
        """Kényelmi megoldás."""
        return self["nem"]
    
    @property
    def megjegyzes(self):
        """Kényelmi megoldás."""
        return self["megjegyzes"]
    
    def listanezet(self):
        """Személy megjelenítése kiválasztáshoz (Combobox)"""
        megjegyzes = self._nullazo(self["megjegyzes"])
        return "{} {} {}{}".format(self["vezeteknev"], self["keresztnev"], self["elotag"], megjegyzes)
    
    def megszolitas(self):
        return "Tisztelt {}!".format("Uram" if self["nem"] == "férfi" else "Hölgyem")

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