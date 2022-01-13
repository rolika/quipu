"""
Very simple company management

MIT License

Copyright (c) 2019 Weisz Roland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import tamer
from konnektor import Konnektor


class Quipu:
    """ Fő alkalmazás
    A kipu, más néven csomóírás vagy zsinórírás egy különleges, tízes számrendszerbeli információtárolási rendszer,
    melynek segítségével helyettesítették az írást az Inka Birodalomban. A kipu a kecsuák nyelvén csomót jelent,
    használati gyakorlatáról bebizonyították, hogy afféle textil abakusz, ahol a csomók jelentést hordoznak.
    A kipukon rögzített értékeket meglepő módon egy kettes számrendszeren alapuló, kövek helyzetével operáló, számoló
    eszközzel, egy ősi számítógéppel dolgozták fel. [Wikipedia nyomán]
    """
    def __init__(self) -> None:

        # adatbázis konnektorok
        kon = Konnektor(
            szemely=self._init_szemely_db("szemely"),
            szervezet=self._init_szervezet_db("szervezet"),
            kontakt=self._init_kontakt_db("kontakt"),
            projekt=self._init_projekt_db("projekt"),
            ajanlat=self._init_ajanlat_db("ajanlat"),
            raktar=self._init_raktar_db("raktar")
            )

    def _init_szemely_db(self, db_file:str) -> tamer.Tamer:
        """Személy adatbázis inicializálása"""
        szemely_kon = tamer.Tamer("db/" + db_file + ".db")

        szemely_kon.create("szemely",
            azonosito="INTEGER PRIMARY KEY",
            elotag="TEXT DEFAULT ''",
            vezeteknev="TEXT NOT NULL",
            keresztnev="TEXT",
            becenev="TEXT",
            nem="TEXT",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        return szemely_kon

    def _init_szervezet_db(self, db_file:str) -> tamer.Tamer:
        """Szervezet adatbázis inicializálása"""
        szervezet_kon = tamer.Tamer("db/" + db_file + ".db")

        szervezet_kon.create("szervezet",
            azonosito="INTEGER PRIMARY KEY",
            rovidnev="TEXT NOT NULL",
            teljesnev="TEXT",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        return szervezet_kon

    def _init_kontakt_db(self, db_file:str) -> tamer.Tamer:
        """Kontaktszemélyek adatbázisának inicializálása"""
        kontakt_kon = tamer.Tamer("db/" + db_file + ".db")

        kontakt_kon.create("kontakt",
            azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER",
            szervezet="INTEGER",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("telefon",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES kontakt",
            telefonszam="TEXT NOT NULL",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("email",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES kontakt",
            emailcim="TEXT NOT NULL",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("cim",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES kontakt",
            orszag="TEXT DEFAULT 'H'",
            megye="TEXT DEFAULT ''",
            iranyitoszam="TEXT DEFAULT ''",
            helyseg="TEXT NOT NULL",
            utca="TEXT DEFAULT ''",
            hrsz="TEXT DEFAULT ''",
            postafiok="TEXT DEFAULT ''",
            honlap="TEXT DEFAULT ''",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("vevo",
            azonosito="INTEGER PRIMARY KEY",
            kontakt="INTEGER UNIQUE REFERENCES kontakt",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("szallito",
            azonosito="INTEGER PRIMARY KEY",
            kontakt="INTEGER UNIQUE REFERENCES kontakt",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        kontakt_kon.create("gyarto",
            azonosito="INTEGER PRIMARY KEY",
            kontakt="INTEGER UNIQUE REFERENCES kontakt",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        return kontakt_kon

    def _init_projekt_db(self, db_file:str) -> tamer.Tamer:
        """Projekt adatbázis inicializálása"""
        projekt_kon = tamer.Tamer("db/" + db_file + ".db")

        projekt_kon.create("projekt",
            azonosito="INTEGER PRIMARY KEY",
            megnevezes="TEXT NOT NULL",
            rovidnev="TEXT",
            ev="INTEGER NOT NULL",
            szam="INTEGER NOT NULL",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        projekt_kon.create("munkaresz",
            azonosito="INTEGER PRIMARY KEY",
            projekt="INTEGER NOT NULL REFERENCES projekt",
            megnevezes="TEXT NOT NULL",
            enaplo="INTEGER",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        projekt_kon.create("cim",
            azonosito="INTEGER PRIMARY KEY",
            munkaresz="INTEGER NOT NULL REFERENCES munkaresz",
            orszag="TEXT DEFAULT 'H'",
            megye="TEXT DEFAULT ''",
            iranyitoszam="TEXT DEFAULT ''",
            helyseg="TEXT NOT NULL",
            utca="TEXT DEFAULT ''",
            hrsz="TEXT DEFAULT ''",
            postafiok="TEXT DEFAULT ''",
            honlap="TEXT DEFAULT ''",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        projekt_kon.create("jelleg",
            azonosito="INTEGER PRIMARY KEY",
            munkaresz="INTEGER NOT NULL REFERENCES munkaresz",
            megnevezes="TEXT NOT NULL",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        return projekt_kon

    def _init_ajanlat_db(self, db_file:str) -> tamer.Tamer:
        """Ajánlat adatbázis inicializálása."""
        ajanlat_kon = tamer.Tamer("db/" + db_file + ".db")

        ajanlat_kon.create("ajanlatkeres",
            azonosito="INTEGER PRIMARY KEY",
            jelleg="INTEGER NOT NULL",
            ajanlatkero="INTEGER NOT NULL",
            temafelelos="INTEGER NOT NULL",
            erkezett="TEXT DEFAULT CURRENT_DATE",
            hatarido="TEXT DEFAULT ''",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        ajanlat_kon.create("ajanlat",
            azonosito="INTEGER PRIMARY KEY",
            ajanlatkeres="INTEGER NOT NULL REFERENCES ajanlatkeres",
            ajanlatiar="INTEGER NOT NULL",
            leadva="TEXT DEFAULT CURRENT_DATE",
            ervenyes="TEXT DEFAULT ''",
            esely="INTEGER DEFAULT 5",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        return ajanlat_kon

    def _init_raktar_db(self, db_file:str) -> tamer.Tamer:
        """Raktárkészlet-adatbázis inicializálása."""
        raktar_kon = tamer.Tamer("db/" + db_file + ".db")

        raktar_kon.create("anyag",
            azonosito="INTEGER PRIMARY KEY",
            gyarto="INTEGER",
            nev="TEXT",
            tipus="TEXT",
            cikkszam="TEXT",
            leiras="TEXT",
            szin="TEXT",
            szinkod = "TEXT",
            egyseg="TEXT",
            kiszereles_nev="TEXT",
            kiszereles="REAL",
            csomagolas_nev="TEXT",
            csomagolas="REAL",
            kritikus="REAL",
            szallitasi_ido="INTEGER",
            eltarthato="INTEGER DEFAULT 0",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT")

        raktar_kon.create("termek",
            azonosito="INTEGER PRIMARY KEY",
            anyag="INTEGER",
            szallito="INTEGER",
            egysegar="INTEGER",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT")

        raktar_kon.create("keszlet",
            azonosito="INTEGER PRIMARY KEY",
            termek="INTEGER",
            mennyiseg="REAL",
            erkezett="DATE",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT")
        
        raktar_kon.create("szallitolevel",
            azonosito="INTEGER PRIMARY KEY",
            jelleg="INTEGER",
            szam="TEXT",
            datum="DATETIME",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT")

        raktar_kon.create("tetel",
            azonosito="INTEGER PRIMARY KEY",
            szallitolevel="INTEGER",
            aru="INTEGER",
            mennyiseg="REAL",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT")
        
        return raktar_kon


if __name__ == "__main__":
    app = Quipu()
