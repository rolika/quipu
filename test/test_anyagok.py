"""Árlista beolvasása az adatbázisba.
Felhasznált funckciók:
    - anyag és
    - termék.
Érintett funkciók:
    - személy,
    - szervezet és
    - kontakt.
Feltételezem, hogy a Quipu már legalább egyszer futott és létrehozta az adatbázis file-okat."""


import unittest
import csv
from collections import namedtuple
from kontakt import Kontakt
from gyarto import Gyarto
from anyag import Anyag
from termek import Termek
from szallito import Szallito
from szervezet import Szervezet
from szemely import Szemely
from tamer import Tamer
from konnektor import Konnektor


class AnyagTest(unittest.TestCase):

    def setUp(self) -> None:
        self._kon = Konnektor(szemely=Tamer("szemely.db"),
                              szervezet=Tamer("szervezet.db"),
                              kontakt=Tamer("kontakt.db"),
                              raktar=Tamer("raktar.db"))

        szemely_azonosito = None
        szervezet_azonosito = None
        szemely = Szemely(vezeteknev="Megrendelés")
        if not szemely.meglevo(self._kon.szemely):
            szemely_azonosito = szemely.ment(self._kon.szemely)
        szervezet = Szervezet(rovidnev="Bauder")
        if not szervezet.meglevo(self._kon.szervezet):
            szervezet_azonosito = szervezet.ment(self._kon.szervezet)
        if szemely_azonosito and szervezet_azonosito:
            kontakt = Kontakt(szemely=szemely_azonosito, szervezet=szervezet_azonosito)
            kontakt_azonosito = kontakt.ment(self._kon.kontakt)
            gyarto = Gyarto(kontakt=kontakt_azonosito)
            self._gyarto = gyarto.ment(self._kon.kontakt)
            szallito = Szallito(kontakt=kontakt_azonosito)
            self._szallito = szallito.ment(self._kon.kontakt)
        else:
            self._gyarto = 1
            self._szallito = 1

    def test_arlista_import(self):
        ArlistaRekord = namedtuple("ArlistaRekord", ["cikkszam", "nev", "leiras", "kiszereles", "csomagolas", "listaar", "egysegar"])

        with open("Bauder_FPO.csv", newline="") as anyagok:
            for rekord in map(ArlistaRekord._make, csv.reader(anyagok, delimiter=",")):
                try:
                    cikkszam = int(rekord.cikkszam)  # csak azok a rekordok érdekesek, melyek cikkszámmal kezdődnek
                except ValueError:
                    continue

                anyag = Anyag(gyarto=self._gyarto, cikkszam=cikkszam, nev=rekord.nev or "kiegészítő", tipus="szigetelőfólia", egyseg="m2", leiras=rekord.leiras, kiszereles=rekord.kiszereles, csomagolas=rekord.csomagolas, megjegyzes="")
                if anyag.meglevo(self._kon.raktar):
                    continue

                anyag_azonosito = anyag.ment(self._kon.raktar)

                termek = Termek(szallito=self._szallito, anyag=anyag_azonosito, egysegar=rekord.egysegar, megjegyzes="")
                if not termek.meglevo(self._kon.raktar):
                    termek.ment(self._kon.raktar)

        return True

