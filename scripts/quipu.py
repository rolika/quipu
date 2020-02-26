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
import sqlite3
import urlap
import menu


class Quipu(Frame):
    """ Fő alkalmazás """
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.init_szemely_db()
        menu.Fomenu(self, self.szemely_kon)
        self.grid()
        self.mainloop()

    def init_szemely_db(self):
        """ Személy adatbázis inicializálása  """
        self.szemely_kon = tamer.Tamer("szemely.db")

        self.szemely_kon.create("szemely", azonosito="INTEGER PRIMARY KEY", elotag="TEXT",
            vezeteknev="TEXT NOT NULL", keresztnev="TEXT NOT NULL", nem="TEXT NOT NULL",
            megjegyzes="TEXT")

        self.szemely_kon.create("telefon", azonosito="INTEGER PRIMARY KEY", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            telefonszam="TEXT NOT NULL", megjegyzes="TEXT")

        self.szemely_kon.create("email", azonosito="INTEGER PRIMARY KEY", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            emailcim="TEXT NOT NULL", megjegyzes="TEXT")

        self.szemely_kon.create("cim", azonosito="INTEGER PRIMARY KEY", szemely="INTEGER NOT NULL REFERENCES szemely ON DELETE CASCADE",
            orszag="TEXT DEFAULT 'H'", iranyitoszam="TEXT", helyseg="TEXT", utca="TEXT", megjegyzes="TEXT")

        self.szemely_kon.create("kontakt", azonosito="INTEGER PRIMARY KEY",
            szemely="INTEGER NOT NULL REFERENCES szemely", szervezet="INTEGER", megjegyzes="TEXT")

        self.szemely_kon.executescript("""
            -- automatikusan add hozzá a kontaktszemélyhez is
            CREATE TRIGGER IF NOT EXISTS kntkt AFTER INSERT ON szemely
                BEGIN
                    INSERT INTO kontakt(szemely) VALUES(last_insert_rowid());
                END;
        """)


if __name__ == "__main__":
    app = Quipu()
