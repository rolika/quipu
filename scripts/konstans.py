""" Különböző konstansok, hogy minden egy helyen és egyszer legyen definiálva"""

from enum import Enum

ELERHETOSEG_TIPUS = ("alapértelmezett", "munkahelyi", "privát")
CIM_TIPUS = ("alapértelmezett", "székhely", "telephely", "levelezési cím", "lakhely", "tartózkodási hely")
BEOSZTAS = ("műszaki előkészítő", "képviselő", "projektvezető", "építésvezető", "csoportvezető", "felvételis", "dolgozó")
JELLEG = ("új", "felújítás", "javítás", "karbantartás", "bővítés", "átalakítás")
MUNKARESZ = ("szigetelés", "lapostető-szigetelés", "alépítményi szigetelés", "terasz-szigetelés")
MEGYE = ("Baranya", "Bács-Kiskun", "Békés", "Borsod-Abaúj-Zemplén", "Budapest", "Csongrád-Csanád", "Fejér",
         "Győr-Moson-Sopron", "Hajdú-Bihar", "Heves", "Jász-Nagykun-Szolnok", "Komárom-Esztergom", "Nógrád", "Pest",
         "Somogy", "Szabolcs-Szatmár-Bereg", "Tolna", "Vas", "Veszprém", "Zala")
ORSZAG = {
            "Magyarország": "H",
            "Németország": "D",
            "Ausztria": "A",
            "Svájc": "CH",
            "Hollandia": "NL",
            "Szlovákia": "SK",
            "Csehország": "CZ",
            "USA": "USA",
            "Románia": "RO"
        }

class Kulcs(Enum):
    """ Az alkalmazás adatbázisában különleges pozíciókat elfoglaló cégek, személyek adatai.
        arg: (kulcs, nev): SQL PRIMARY KEY-t és megnevezést tartalmazó tuple. """
    MAGANSZEMELY = (1, "#magánszemély")  # SQL PRIMARY KEY = 1 a szervezetek között (mint rövid név)
    JOGISZEMELY = (1, "#jogi személy")  # SQL PRIMARY KEY = 1 a személyek között (mint vezetéknév)
    CEG = (2, "Pohlen-Dach Hungária Bt.")  # SQL PRIMARY KEY = 2 a felhasználó cég a szervezetek között (rövid név)
    JOGI_MAGAN = 1

    def __init__(self, kulcs, nev):
        """A tuple kibontása automatikus."""
        self._kulcs = kulcs
        self._nev = nev
    
    @property
    def kulcs(self):
        return self._kulcs
    
    @property
    def nev(self):
        return self._nev

if __name__ == "__main__":
    """Használatot bemutató példák, ill. jelmagyarázat."""
    print("Magánszemély megnevezése: {}, és SQL-kulcsa: {}.".format(Kulcs.MAGANSZEMELY.nev, Kulcs.MAGANSZEMELY.kulcs))
    print("Jogi személy megnevezése: {}, és SQL-kulcsa: {}.".format(Kulcs.JOGISZEMELY.nev, Kulcs.JOGISZEMELY.kulcs))
    print("Felhasználó cég neve: {}, és SQL-kulcsa: {}.".format(Kulcs.CEG.nev, Kulcs.CEG.kulcs))