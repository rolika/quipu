import re


class Csomo:
    """A kipu egy csomóírás. Ez az alkalmazás is alapvető csomókból áll."""

    def ascii_rep(szoveg) -> str:
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről, sorbarendezéshez
        szoveg:     string"""
        return "".join(re.findall("[a-z]", szoveg.lower().translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))))

    def formazo(attr, zarojel="()", elvalasztojel=" ", hatul=False) -> str:
        """Segít a formázásban, ill. ha hiányzik az adat, nem írjuk ki egyáltalán.
        attr:           attribútum, vagy annak hiánya, ha üres
        zarojel:        () vagy [] vagy {} esetleg // vagy "" legyen az adat körül (két karakter legyen, vagy üres)
        elvalasztojel:  az adatot a többitől elválasztó jel
        hatul:          az elválasztójel hátul legyen"""
        if attr == "None":
            return ""
        if hatul:
            hatul = elvalasztojel
            elvalasztojel = ""
        else:
            hatul = ""
        nyito = zarojel[0] if zarojel else ""
        zaro = zarojel[1] if zarojel else ""
        return "{elvalaszto}{nyit}{adat}{zar}{hatul}"\
            .format(elvalaszto=elvalasztojel, nyit=nyito, adat=attr, zar=zaro, hatul=hatul) if attr else ""

    def __init__(self, kon=None, db=None, tabla=None) -> object:
        """A csomó bázispéldánya. Önmagában nem jó semmire, le kell származtatni.
        kon:    Konnektor() adabázis-gyűjtőkapcsolat
        db:     a csomóhoz tartozó adatbázis-file
        tabla:  a csomóhoz tartozó tábla"""
        self._adatok = dict()
        self._kon = kon
        self._db = db
        self._tabla = tabla

    @classmethod
    def egy(cls, kon, azonosito):
        """Egy meglévő, adott azonosítójú csomó előkeresése az adatbázisból. Factory metódus.
        kon:        Konnektor adatbázis-kapcsolat
        azonosito:  SQL PRIMARY KEY"""
        csomo = kon[cls.db].select(cls.tabla, azonosito=azonosito).fetchone()
        return cls(kon=kon, **csomo)

    @classmethod
    def osszes(cls, kon) -> list:
        """Az összes adott típusú csomó előkeresése az adatbázisból.
        kon:        Konnektor adatbázis-kapcsolat"""
        return sorted(map(lambda csomo: cls(kon=kon, **csomo), kon[cls.db].select(cls.tabla)), key=repr)

    def __str__(self) -> str:
        """Csomó miden adatának szöveges megjelenítése, terminál-nézethez."""
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
    def gyakorisag(self) -> int:
        """A csomó használatának gyakorisága."""
        return self._adatok.get("gyakorisag", 0)

    @property
    def megjegyzes(self) -> str:
        """Minden csomóhoz fűzhető valamilyen megjegyzés."""
        return self._adatok.get("megjegyzes")

    def listanezet(self) -> str:
        """Csomó szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        raise NotImplementedError

    def meglevo(self) -> bool:
        """Ellenőrzi, hogy a csomó szerepel-e az adatbázisban."""
        assert self._kon
        assert self._db
        assert self._tabla
        csomo = self._kon[self._db].select(self._tabla, logic="AND", **self._adatok)
        return True if self.azonosito else csomo.fetchone()

    def ment(self) -> bool:
        """Menti vagy módosítja a csomó adatait, attól függően, van-e azonosítója, jelezve, sikerült-e a művelet:
        return:
            True:       sikerült a módosítás
            False:      nem sikerült a módosítás (alapvetően adatbázis-hiba)
            lastrowid:  sikerült az új csomó adatainak mentése (utolsó insert sql primary key)
            None:       nem sikerült az új csomó adatainak mentése (alapvetően adatbázis-hiba)"""
        assert self._kon
        assert self._db
        assert self._tabla
        if self.azonosito:
            muvelet = self._kon[self._db].update(self._tabla, self._adatok, azonosito=self.azonosito)
        else:
            muvelet = self._kon[self._db].insert(self._tabla, **self._adatok)
        if muvelet:
            self._adatok["gyakorisag"] = self.gyakorisag - 1
        return muvelet

    def torol(self) -> bool:
        """Törli az adatbázisból a csomó adatait, jelezve, hogy sikerült-e a törlés."""
        assert self._kon
        assert self._db
        assert self._tabla
        return self._kon[self._db].delete(self._tabla, azonosito=self.azonosito)