class Csomo:
    """A kipu egy csomóírás. Ez az alkalmazás is alapvető csomókból áll."""
    def __init__(self):
        self._adatok = dict()
        self._tabla = None
        self._szemely_kon = None
        self._szervezet_kon = None
        self._kontakt_kon = None
        self._projekt_kon = None
        self._ajanlat_kon = None

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
    
    @property
    def szemely_kon(self):
        return self._szemely_kon
    
    @szemely_kon.setter
    def szemely_kon(self, kon):
        self._szemely_kon = kon
    
    @property
    def szervezet_kon(self):
        return self._szervezet_kon
    
    @szervezet_kon.setter
    def szervezet_kon(self, kon):
        self._szervezet_kon = kon
    
    @property
    def kontakt_kon(self):
        return self._kontakt_kon
    
    @kontakt_kon.setter
    def kontakt_kon(self, kon):
        self._kontakt_kon = kon
    
    @property
    def projekt_kon(self):
        return self._projekt_kon
    
    @projekt_kon.setter
    def projekt_kon(self, kon):
        self._projekt_kon = kon
    
    @property
    def ajanlat_kon(self):
        return self._ajanlat_kon
    
    @projekt_kon.setter
    def ajanlat_kon(self, kon):
        self._ajanlat_kon = kon

    def listanezet(self):
        """Csomó szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        raise NotImplementedError

    def meglevo(self, kon):
        """Ellenőrzi, hogy a csomó szerepel-e az adatbázisban.
        kon:    tamer modul adatbázis konnektora"""
        return True if self.azonosito else kon.select(self._tabla, logic="AND", **self._adatok).fetchone()

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

    def _nullazo(self, attr, zarojel="()", elvalasztojel=" "):
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
