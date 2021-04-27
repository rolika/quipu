from konnektor import Konnektor  # csak function annotation miatt


class Csomo:
    """A kipu egy csomóírás. Ez az alkalmazás is alapvető csomókból áll."""
    def __init__(self, kon=None) -> object:
        """A csomó bázispéldánya. Önmagában nem jó semmire, a le kell származtatni.
        kon:    Konnektor() adabázis-gyűjtőkapcsolat"""
        self._adatok = dict()
        self._tabla = None
        self._kon = kon

    def __str__(self) -> str:
        """Csomó szöveges megjelenítése, elsősorban debugoláshoz."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Csomó neve sorbarendezéshez, jellemzően kisbetűs, ékezetek nélkül, ld. self._ascii_rep()."""
        raise NotImplementedError

    def __bool__(self) -> bool:
        """A csomó elegendően meghatározott-e, azaz a felhasználó elég adatot adott meg vagy sem."""
        raise NotImplementedError
    
    def __eq__(self, masik) -> bool:
        """A csomó azonos egy másikkal, ha azonos az SQL PRIMARY KEY-ük.
        Kell a None-check, mert None == None True-t ad."""
        return False if self.azonosito is None else self.azonosito == masik.azonosito

    @property
    def azonosito(self) -> int:
        """A csomó azonosítója (SQL PRIMARY KEY)."""
        return self._adatok.get("azonosito")
    
    @azonosito.setter
    def azonosito(self, azonosito) -> None:
        """A csomó azonosítójának (SQL PRIMARY KEY) beállítása kívülről."""
        self._adatok["azonosito"] = azonosito

    @property
    def megjegyzes(self) -> str:
        """Minden csomóhoz fűzhető valamilyen megjegyzés."""
        return self._adatok.get("megjegyzes")

    def listanezet(self) -> str:
        """Csomó szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        raise NotImplementedError

    def meglevo(self, kon) -> bool:
        """Ellenőrzi, hogy a csomó szerepel-e az adatbázisban.
        kon:    tamer modul adatbázis konnektora"""
        return True if self.azonosito else kon.select(self._tabla, logic="AND", **self._adatok).fetchone()

    def ment(self, kon) -> bool:
        """Menti vagy módosítja a csomó adatait.
        kon:    tamer modul adatbázis konnektora"""
        if self.azonosito:
            return kon.update(self._tabla, self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert(self._tabla, **self._adatok)  # lastrowid vagy None

    def torol(self, kon) -> bool:
        """Törli az adatbázisból a csomót.
        kon:    tamer modul adatbázis konnektora"""
        return kon.delete(self._tabla, azonosito=self.azonosito)

    def _ascii_rep(self, szoveg) -> str:
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))

    def _nullazo(self, attr, zarojel="()", elvalasztojel=" ") -> str:
        """Ha hiányzik az adat, nem írjuk ki egyáltalán.
        attr:           attribútum, vagy annak hiánya, ha üres
        zarojel:        () vagy [] vagy {} esetleg // vagy "" legyen az adat körül (két karakter legyen, vagy üres)
        elvalasztojel:  az adatot a többitől elválasztó jel"""
        if attr == "None":
            return ""
        nyito = zarojel[0] if zarojel else ""
        zaro = zarojel[1] if zarojel else ""
        return "{elvalaszto}{nyit}{adat}{zar}"\
            .format(elvalaszto=elvalasztojel, nyit=nyito, adat=attr, zar=zaro) if attr else ""
