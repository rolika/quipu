class Telefon(dict):
    """Telefonos elérhetőség megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor közvetlen példányosításhoz:
        kwargs:     adatok kulcs=érték párokként"""
        super().__init__(kwargs)
        for oszlop in ("azonosito", "szemely", "telefonszam", "megjegyzes"):
            self[oszlop] = kwargs.get(oszlop, "")
    
    def __bool__(self):
        """Telefonszámot kötelező megadni."""
        return bool(self.telefonszam) 

    @classmethod
    def adatbazisbol(cls, row):
        """Factory konstruktor adatbázisból történő példányososításhoz:
        row:    sqlite Row-objektum (hozzáférés oszlopnevekkel)"""
        return cls(**row)
    
    @property
    def azonosito(self):
        """Kényelmi megoldás."""
        return self["azonosito"]

    
    @property
    def szemely(self):
        """Kényelmi megoldás."""
        return self["szemely"]
    
    @property
    def telefonszam(self):
        """Kényelmi megoldás."""
        return self["telefonszam"]
    
    @property
    def megjegyzes(self):
        """Kényelmi megoldás."""
        return self["megjegyzes"]
    
    @szemely.setter
    def szemely(self, szemely):
        self["szemely"] = szemely
    
    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{} ({})".format(self.telefonszam, self.megjegyzes)