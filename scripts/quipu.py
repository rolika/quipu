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
import sqlite3
import szemelyform


class Quipu:
    """ Fő alkalmazás """
    def __init__(self):
        self.szemely_init()

    def szemely_init(self):
        """ Személy adatbázis inicializálása  """
        self.szemely_kon = tamer.Tamer("szemely.db")

        self.szemely_kon.create("megszolitas", nem="TEXT PRIMARY KEY", megszolitas="TEXT NOT NULL")
        self.szemely_kon.insert("megszolitas", nem="nő", megszolitas="Hölgyem")
        self.szemely_kon.insert("megszolitas", nem="férfi", megszolitas="Uram")

        self.szemely_kon.create("szemely", azonosito="INTEGER PRIMARY KEY", elotag="TEXT",
            vezeteknev="TEXT NOT NULL", keresztnev="TEXT NOT NULL", nem="TEXT NOT NULL REFERENCES megszolitas",
            megjegyzes="TEXT")

        self.szemely_kon.create("telefon", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            telefonszam="TEXT NOT NULL", megjegyzes="TEXT DEFAULT 'elsődleges'")

        self.szemely_kon.create("email", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            emailcim="TEXT NOT NULL", megjegyzes="TEXT DEFAULT 'elsődleges'")

        self.szemely_kon.create("cim", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            orszag="TEXT DEFAULT 'H'", iranyitoszam="TEXT", helyseg="TEXT", utca="TEXT",
            megjegyzes="TEXT DEFAULT 'elsődleges'")

        self.szemely_kon.create("kontakt", azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER NOT NULL REFERENCES szemely", szervezet="INTEGER", megjegyzes="TEXT")

        self.szemely_kon.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE VIEW IF NOT EXISTS nev(szemely, nev) AS
                SELECT azonosito, ltrim(printf('%s %s %s', elotag, vezeteknev, keresztnev))
                    FROM szemely;

            CREATE VIEW IF NOT EXISTS teljescim(szemely, cim) AS
                SELECT szemely, printf('%s-%s %s, %s', orszag, iranyitoszam, helyseg, utca)
                    FROM cim;

            CREATE VIEW IF NOT EXISTS elerhetoseg(szemely, elerhetoseg) AS
                SELECT nev.szemely, printf('%s: %s, %s', nev, telefonszam, emailcim)
                    FROM nev, telefon, email
                        WHERE nev.szemely=telefon.szemely
                            AND nev.szemely=email.szemely
                            AND telefon.megjegyzes='elsődleges'
                            AND email.megjegyzes='elsődleges';

            CREATE VIEW IF NOT EXISTS koszontes(szemely, koszontes) AS
                SELECT szemely.azonosito, printf('Tisztelt %s!', megszolitas)
                    FROM szemely, megszolitas
                        WHERE szemely.nem=megszolitas.nem;

            -- automatikusan add hozzá a kontaktszemélyhez is
            CREATE TRIGGER IF NOT EXISTS kntkt AFTER INSERT ON szemely
                BEGIN
                    INSERT INTO kontakt(szemely) VALUES(last_insert_rowid());
                END;
        """)

    def uj_szemely(self):
        ablak = szemelyform.SzemelyForm()
        ablak.mainloop()
        if ablak.valasztas == "mentés":
            return self.szemely_kon.insert("szemely", **ablak.export())
        return None
    
    def szemely_modositasa(self, azonosito):      
        urlap = szemelyform.SzemelyForm()
        szemely = self.szemely_kon.select("szemely", azonosito=azonosito)
        szemely = szemely.fetchone()
        if szemely:
            szemely = {mezo: szemely[mezo] for mezo in urlap.mezo if szemely[mezo]}
        urlap.felulir(**szemely)
        urlap.mainloop()
        if urlap.valasztas == "mentés":
            return self.szemely_kon.update("szemely", urlap.export(), azonosito=azonosito)
        elif urlap.valasztas == "törlés":
            return self.szemely_kon.delete("szemely", azonosito=azonosito)
        return None
    
    def szemely_email(self):
        pass


if __name__ == "__main__":
    app = Quipu()
    if app.szemely_modositasa(18):
        print("bejegyzés módosítva")
    app.szemely_kon.close()