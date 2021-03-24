import copy


class Csomo:
    """A kipu egy csomóírás. Ez az alkalmazás is alapvető csomókból áll."""
    def __init__(self):
        self._adatok = dict()
        self._tabla = None

    def __str__(self):
        """Csomó szöveges megjelenítése, elsősorban debugoláshoz."""
        raise NotImplementedError

    def __repr__(self):
        """Csomó neve sorbarendezéshez, jellemzően kisbetűs, ékezetek nélkül, ld. self._ascii_rep()."""
        raise NotImplementedError

    def __bool__(self):
        """A csomó elegendően meghatározott-e, azaz a felhasználó elég adatot adott meg vagy sem."""
        raise NotImplementedError

    @property
    def azonosito(self):
        """A csomó azonosítója (SQL PRIMARY KEY)."""
        return self._adatok.get("azonosito")
    
    @azonosito.setter
    def azonosito(self, azonosito):
        """A csomó azonosítójának (SQL PRIMARY KEY) beállítása kívülről."""
        self._adatok["azonosito"] = azonosito

    @property
    def megjegyzes(self):
        """Minden csomóhoz fűzhető valamilyen megjegyzés."""
        return self._adatok.get("megjegyzes")

    def listanezet(self):
        """Csomó szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        raise NotImplementedError

    def meglevo(self, kon):
        """Ellenőrzi, hogy a csomó szerepel-e az adatbázisban.
        kon:    tamer modul adatbázis konnektora"""
        adatok = copy.copy(self._adatok)  # shallow copy
        adatok.pop("azonosito", None)
        return kon.select(self._tabla, logic="AND", **adatok).fetchone()

    def ment(self, kon):
        """Menti vagy módosítja a csomó adatait.
        kon:    tamer modul adatbázis konnektora"""
        if self.azonosito:
            return kon.update(self._tabla, self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert(self._tabla, **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból a csomót.
        kon:    tamer modul adatbázis konnektora"""
        return kon.delete(self._tabla, azonosito=self.azonosito)

    def _ascii_rep(self, szoveg):
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))

    def _nullazo(self, attr):
        """Ha hiányzik az adat, nem írjuk ki egyáltalán.
        attr:   attribútum, vagy annak hiánya, ha üres"""
        return " ({})".format(attr) if attr else ""
