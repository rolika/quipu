""" Különböző konstansok, hogy minden egy helyen és egyszer legyen definiálva"""


from szemely import Szemely
from szervezet import Szervezet
import enum


ELERHETOSEG_TIPUS = ("alapértelmezett", "munkahelyi", "privát")
CIM_TIPUS = ("alapértelmezett", "székhely", "telephely", "levelezési cím", "lakhely", "tartózkodási hely")
BEOSZTAS = ("műszaki előkészítő", "képviselő", "projektvezető", "építésvezető", "csoportvezető", "felvételis", "dolgozó")
JELLEG = ("új", "felújítás", "javítás", "karbantartás", "bővítés", "átalakítás", "anyageladás")
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
TERMEK_TIPUS = ("szigetelés", "rezsi", "vízszigetelés", "kötőelem", "hőszigetelés", "párazárás", "szórás", "kiegészítők")


# a magánszemély egy különleges szervezet, hogy a magánszemélyek is kontaktok lehessenek
MAGANSZEMELY = Szervezet(rovidnev="#magánszemély",
                         teljesnev="")

WEVIK = Szervezet(rovidnev="Wevik Engineer Kft.",
                  teljesnev="Wevik Engineer Kft.")

VITYA = Szemely(vezeteknev="Weisz",
                keresztnev="Viktor",
                nem="férfi")

ROLI = Szemely(vezeteknev="Weisz",
               keresztnev="Roland",
               nem="férfi")


class Esely(enum.IntEnum):
    """Ajánlat elnyerésének esélye."""
    BUKOTT = 0
    NORMAL = 5
    ERDEKES = 50
    VEGSO = 90

    @property
    def ertek(self):
        return self.value

