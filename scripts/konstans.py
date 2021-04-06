""" Különböző konstansok, hogy minden egy helyen és egyszer legyen definiálva"""


from szemely import Szemely
from szervezet import Szervezet


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

# a magánszemély egy különleges szervezet, hogy a magánszemélyek is kontaktok lehessenek
MAGANSZEMELY = Szervezet(azonosito=1,
                         rovidnev="#magánszemély",
                         teljesnev="")

WEVIK = Szervezet(azonosito=2,
                  rovidnev="Wevik Engineer Kft.", 
                  teljesnev="Wevik Engineer Kft.")

VITYA = Szemely(azonosito=1,
                vezeteknev="Weisz",
                keresztnev="Viktor",
                nem="férfi")

ROLI = Szemely(azonosito=2,
               vezeteknev="Weisz",
               keresztnev="Roland",
               nem="férfi")