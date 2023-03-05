import re
from datetime import datetime

from code.konnektor import Konnektor
from code.hibakezeles import MeglevoCsomoError


class Csomo:
    """A kipu egy csomóírás, ezért az alkalmazás is alapvető csomókból áll."""

    # osztálymetódusok
    def ascii_rep(szoveg) -> str:
        """Kisbetűs, ékezet nélküli szöveget készít a bemenetről,
        sorbarendezéshez.
        szoveg:     string"""
        return "".join(re.findall("[a-z1-9]", szoveg.lower().\
            translate(str.maketrans("áéíóöőúüű", "aeiooouuu"))))

    def formazo(attr, zarojel="()", elvalasztojel=" ", hatul=False) -> str:
        """Segít a formázásban, ill. ha hiányzik az adat, nem írjuk ki
        egyáltalán.
        attr:           attribútum, vagy annak hiánya, ha üres
        zarojel:        () vagy [] vagy {} esetleg // vagy "" legyen az adat
                        körül (két karakter legyen, vagy üres)
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
            .format(elvalaszto=elvalasztojel,
                    nyit=nyito,
                    adat=attr,
                    zar=zaro,
                    hatul=hatul) if attr else ""

    # osztályváltozók
    kon = Konnektor()

    def __init__(self, kon=None) -> None:
        """A csomó bázispéldánya, le kell származtatni.
        kon:    Konnektor() adabázis-gyűjtőkapcsolat"""
        self._adatok = dict()
        self._db = None
        self._tabla = None

    @classmethod
    def azonositobol(cls, db, tabla, azonosito):
        """Azonosító alapján előkeríti a csomót az adatbázisból."""
        adatok = Csomo.kon[db].select(tabla, azonosito=azonosito).fetchone()
        return cls(**adatok)

    def __str__(self) -> str:
        """Csomó miden adatának szöveges megjelenítése, terminál-nézethez."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Csomó neve sorbarendezéshez, jellemzően kisbetűs, ékezetek nélkül,
        ld. ascii_rep()."""
        raise NotImplementedError

    def __bool__(self) -> bool:
        """A csomó elegendően meghatározott-e, azaz a felhasználó elég adatot
        adott meg vagy sem."""
        raise NotImplementedError

    def __eq__(self, masik) -> bool:
        """A csomó azonos egy másikkal, ha minden jellemző értékük azonos."""
        return self.ertekek == masik.ertekek

    @property
    def azonosito(self) -> int:
        """A csomó azonosítója (SQL PRIMARY KEY)."""
        return self._adatok.get("azonosito")

    @azonosito.setter
    def azonosito(self, azonosito:int) -> None:
        """A csomó azonosítójának (SQL PRIMARY KEY) beállítása kívülről."""
        self._adatok["azonosito"] = azonosito

    @property
    def megjegyzes(self) -> str:
        """Minden csomóhoz fűzhető valamilyen megjegyzés."""
        return self._adatok.get("megjegyzes")

    @megjegyzes.setter
    def megjegyzes(self, megjegyzes:str) -> None:
        """A csomóhoz fűzött megjegyzés beállítása kívülről."""
        self._adatok["megjegyzes"] = megjegyzes

    @property
    def ertekek(self):
        """A csomó minden adata, kivéve azonosító, gyakoriság, létrehozva,
        módosítva. Összehasonlításhoz."""
        return {kulcs: ertek for kulcs, ertek in self._adatok.items()\
                if kulcs not in Csomo.kon.alap_oszlopok}

    def listanezet(self) -> str:
        """Csomó szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        raise NotImplementedError

    def meglevo(self) -> bool:
        """Ellenőrzi, hogy a csomó szerepel-e az adatbázisban."""
        talalat = self.keres(**self.ertekek).fetchone()
        return True if talalat else False

    def ment(self) -> bool:
        """Menti vagy módosítja a csomó adatait."""
        assert self._db
        assert self._tabla
        if self.meglevo():
            raise MeglevoCsomoError
        idobelyeg = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        self._adatok["modositva"] = idobelyeg
        if self.azonosito:  # módosítás: True vagy False
            return Csomo.kon[self._db].\
                update(self._tabla, self._adatok, azonosito=self.azonosito)
        else:  # új rekord: lastrowid vagy None
            self._adatok["letrehozva"] = idobelyeg
            return Csomo.kon[self._db].insert(self._tabla, **self._adatok)

    def torol(self) -> bool:
        """Törli az adatbázisból a csomót."""
        assert self._db
        assert self._tabla
        return Csomo.kon[self._db].delete(self._tabla, azonosito=self.azonosito)

    def keres(self, **kwargs):
        """Rákeres a megadott kulcsszavakra az adatbázisban."""
        assert self._db
        assert self._tabla
        return Csomo.kon[self._db].select(self._tabla, logic= "AND", **kwargs)