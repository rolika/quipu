class Dolog:
    """Nyilvántartott dolgok alaposztálya."""
    def __init__(self, **kwargs):
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = None
        self._adatok = dict()
        self._tabla = None
    
    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError
    
    @property
    def adatok(self):
        return self._adatok
    
    @adatok.setter
    def adatok(self, **kwargs):        
        raise NotImplementedError

    @property
    def tabla(self):
        return self._tabla
    
    @tabla.setter
    def tabla(self, nev):
        self._tabla = nev

    @property
    def azonosito(self):
        return self._adatok.get("azonosito")
    
    @property
    def megjegyzes(self):
        return self._adatok.get("megjegyzes")

    def listanezet(self):
        """Szervezet megjelenítése kiválasztáshoz (Combobox)"""
        raise NotImplementedError

    def meglevo(self, kon):
        """Ellenőrzi, hogy a szervezet szerepel-e az adatbázisban"""
        adatok = copy.copy(self._adatok)  # shallow copy
        adatok.pop("azonosito", None)
        return kon.select(self._tabla, logic="AND", **adatok).fetchone()

    def ment(self, kon):
        """Menti vagy módosítja a dolog adatait"""
        if self.azonosito:
            return kon.update(self._tabla, self._adatok, azonosito=self.azonosito)  # True vagy False
        else:
            return kon.insert(self._tabla, **self._adatok)  # lastrowid vagy None

    def torol(self, kon):
        """Törli az adatbázisból a dolog-bejegyzést"""
        return kon.delete(self._tabla, azonosito=self.azonosito)
    
    def _ascii_rep(self, szoveg):
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))
    
    def _nullazo(self, attr):
        """Ha hiányzik az adat, nem írjuk ki egyáltalán."""
        return ", {}".format(attr) if attr else ""
    