class Szemely:
    """ Személy megvalósítása """
    def __init__(self, **kwargs):
        """Konstruktor közvetlen példányosításhoz:
        kwargs:     személyi adatok kulcs=érték párokként"""
        self._db_oszlop = {"elotag", "vezeteknev", "keresztnev", "nem", "megjegyzes"}
        for oszlop in self._db_oszlop:
            setattr(self, "_"+oszlop, kwargs.get(oszlop, ""))

    @classmethod
    def adatbazisbol(cls, kurzor):
        """Factory konstruktor adatbázisból történő példányososításhoz:
        kurzor:     sqlite Row-kurzor (hozzáférés oszlopnevekkel)"""
        return cls(**kurzor.fetchone())
    
    def __str__(self):
        """Személyi adatok megjelenítése, elsősorban debugoláshoz"""
        elotag = self._nullazo(self._elotag)
        megjegyzes = self._nullazo(self._megjegyzes)
        return "{}{} {}, {}{}".format(elotag, self._vezeteknev, self._keresztnev, self._nem, megjegyzes)
    
    def __repr__(self):
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.listanezet())
    
    def __bool__(self):
        """Egy személy akkor meghatározott, ha legalább az egyik név adott"""
        return bool(self._vezeteknev) or bool(self._keresztnev)
    
    def listanezet(self):
        """Személy megjelenítése kiválasztáshoz (pl. Combobox)"""
        return "{} {} {}{}".format(self._vezeteknev, self._keresztnev, self._elotag, self._nullazo(self._megjegyzes))
    
    def megszolitas(self):
        return "Tisztelt {}!".format("Uram" if self._nem == "férfi" else "Hölgyem")

    def _ascii_rep(self, szoveg):
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))
    
    def _nullazo(self, attr):
        """Ha hiányzik az adat, nem írjuk ki egyáltalán."""
        return ", {}".format(attr) if attr else ""


if __name__ == "__main__":
    """Tesztelés"""
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
    szemely = Szemely.adatbazisbol(kon.select("szemely"))
    print(szemely)  # a lekérdezés első bejegyzését kell kiírnia