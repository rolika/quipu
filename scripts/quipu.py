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

from tkinter import *
import tamer
import menu
from konstans import MAGANSZEMELY, WEVIK, VITYA, ROLI
from kontakt import Kontakt


class Quipu(Frame):
    """ Fő alkalmazás 
    A kipu, más néven csomóírás vagy zsinórírás egy különleges, tízes számrendszerbeli információtárolási rendszer,
    melynek segítségével helyettesítették az írást az Inka Birodalomban. A kipu a kecsuák nyelvén csomót jelent, 
    használati gyakorlatáról bebizonyították, hogy afféle textil abakusz, ahol a csomók jelentést hordoznak.
    A kipukon rögzített értékeket meglepő módon egy kettes számrendszeren alapuló, kövek helyzetével operáló, számoló
    eszközzel, egy ősi számítógéppel dolgozták fel. [Wikipedia nyomán]
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        # adatbázis konnektorok
        szemely_kon = self._init_szemely_db()
        szervezet_kon = self._init_szervezet_db()
        kontakt_kon = self._init_kontakt_db()
        projekt_kon = self._init_projekt_db()
        ajanlat_kon = self._init_ajanlat_db()

        # alapadatok beírása
        #if not WEVIK.meglevo(szervezet_kon):  # feltételezem, hogy a céggel együtt a többet se írta még be
        MAGANSZEMELY.ment(szervezet_kon)  # SQL PRIMARY KEY 1
        wevik_id = WEVIK.ment(szervezet_kon)  # SQL PRIMARY KEY 2
        vitya = VITYA.ment(szemely_kon)  # SQL PRIMARY KEY 1
        roli = ROLI.ment(szemely_kon)  # SQL PRIMARY KEY 2
        Kontakt(szemely=vitya, szervezet=wevik_id).ment(kontakt_kon)
        Kontakt(szemely=roli, szervezet=wevik_id).ment(kontakt_kon)

        # főmenü megjelenítése
        menu.Fomenu(self, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon, ajanlat_kon)
        self.grid()

        # és pörgés :-)
        self.mainloop()

    def _init_szemely_db(self):
        """ Személy adatbázis inicializálása  """
        szemely_kon = tamer.Tamer("szemely.db")

        szemely_kon.create("szemely",
            azonosito="INTEGER PRIMARY KEY",
            elotag="TEXT DEFAULT ''",
            vezeteknev="TEXT NOT NULL",
            keresztnev="TEXT",
            becenev="TEXT",
            nem="TEXT",
            megjegyzes="TEXT DEFAULT ''")

        szemely_kon.create("telefon",
            azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            telefonszam="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        szemely_kon.create("email",
            azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            emailcim="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        szemely_kon.create("cim",
            azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            orszag="TEXT DEFAULT 'H'",
            megye="TEXT DEFAULT ''",
            iranyitoszam="TEXT DEFAULT ''",
            helyseg="TEXT NOT NULL",
            utca="TEXT DEFAULT ''",
            hrsz="TEXT DEFAULT ''",
            postafiok="TEXT DEFAULT ''",
            honlap="TEXT DEFAULT ''",
            megjegyzes="TEXT DEFAULT ''")
                                
        return szemely_kon

    def _init_szervezet_db(self):
        """Szervezet adatbázis inicializálása"""
        szervezet_kon = tamer.Tamer("szervezet.db")

        szervezet_kon.create("szervezet",
            azonosito="INTEGER PRIMARY KEY",
            rovidnev="TEXT NOT NULL",
            teljesnev="TEXT",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")

        szervezet_kon.create("telefon",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES szervezet",
            telefonszam="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        szervezet_kon.create("email",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES szervezet",
            emailcim="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        szervezet_kon.create("cim",
            azonosito="INTEGER PRIMARY KEY",
            szervezet="INTEGER NOT NULL REFERENCES szervezet",
            orszag="TEXT DEFAULT 'H'",
            megye="TEXT DEFAULT ''",
            iranyitoszam="TEXT DEFAULT ''",
            helyseg="TEXT NOT NULL",
            utca="TEXT DEFAULT ''",
            hrsz="TEXT DEFAULT ''",
            postafiok="TEXT DEFAULT ''",
            honlap="TEXT DEFAULT ''",
            megjegyzes="TEXT DEFAULT ''")

        return szervezet_kon

    def _init_kontakt_db(self):
        """Kontaktszemélyek adatbázisának inicializálása"""
        kontakt_kon = tamer.Tamer("kontakt.db")

        kontakt_kon.create("kontakt",
            azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER",
            szervezet="INTEGER",
            gyakorisag="INTEGER DEFAULT 0",
            megjegyzes="TEXT DEFAULT ''")
        
        kontakt_kon.create("beosztas",
            azonosito="INTEGER PRIMARY KEY",
            kontakt="INTEGER REFERENCES kontakt",
            megnevezes="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        return kontakt_kon

    def _init_projekt_db(self):
        """Projekt adatbázis inicializálása"""
        projekt_kon = tamer.Tamer("projekt.db")

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
            megjegyzes="TEXT DEFAULT ''")

        projekt_kon.create("jelleg",
            azonosito="INTEGER PRIMARY KEY",
            munkaresz="INTEGER NOT NULL REFERENCES munkaresz",
            megnevezes="TEXT NOT NULL",
            megjegyzes="TEXT DEFAULT ''")

        return projekt_kon

    def _init_ajanlat_db(self):
        """Ajánlat adatbázis inicializálása"""
        ajanlat_kon = tamer.Tamer("ajanlat.db")

        ajanlat_kon.create("ajanlatkeres",
            azonosito="INTEGER PRIMARY KEY",
            jelleg="INTEGER NOT NULL",
            ajanlatkero="INTEGER NOT NULL",
            temafelelos="INTEGER NOT NULL",
            erkezett="TEXT DEFAULT ''",
            hatarido="TEXT DEFAULT ''",
            megjegyzes="TEXT DEFAULT ''")
        
        ajanlat_kon.create("ajanlat",
            azonosito="INTEGER PRIMARY KEY",
            ajanlatkeres="INTEGER NOT NULL REFERENCES ajanlatkeres",
            ajanlatiar="REAL",
            leadva="TEXT DEFAULT ''",
            ervenyes="INTEGER DEFAULT 30",
            esely="REAL DEFAULT 0.05",
            megjegyzes="TEXT DEFAULT ''")
    
        return ajanlat_kon


if __name__ == "__main__":
    app = Quipu()
