"""
Egy meglévő projektlista importálásával tesztelem az eddigi funkciókat:
- személy
- szervezet
- kontakt
- projekt
- ajánlat
Mindre szükség van az importhoz.
Feltételezem, hogy a Quipu már legalább egyszer futott és létrehozta az adatbázis file-okat.
"""


import unittest
import csv
from collections import namedtuple
from tamer import Tamer
from szemely import Szemely
from telefon import Telefon
from email import Email
from szervezet import Szervezet
from kontakt import Kontakt
from projekt import Projekt
from munkaresz import Munkaresz
from ajanlatkeres import Ajanlatkeres
from ajanlat import Ajanlat
from konstans import Kulcs


class ProjektlistaTest(unittest.TestCase):
    """Adatbázis feltöltése projektlistából"""

    def setUp(self) -> None:
        self._szemely_kon = Tamer("szemely.db")
        self._szervezet_kon = Tamer("szervezet.db")
        self._kontakt_kon = Tamer("kontakt.db")
        self._projekt_kon = Tamer("projekt.db")
        self._ajanlat_kon = Tamer("ajanlat.db")

    def test_projektlista_import(self):
        ProjektRekord = namedtuple("ProjektRekord", ["szam", "nev", "helyseg", "orszag", "ar", "esely", "temafelelos",
                                   "szervezet", "szemely", "telefonszam", "emailcim"])
        with open("projektlista.csv", newline='') as projektek:
            for projekt in map(ProjektRekord._make, csv.reader(projektek, delimiter=";")):
                szemely_id = None
                szervezet_id = None
                kontakt_id = None
                projekt_id = None
                munkaresz_id = None
                ajanlatkeres_id = None
                # személyek
                vnev, knev = projekt.szemely.split(" ", maxsplit=1)
                szemely = Szemely(vezeteknev=vnev, keresztnev=knev, megjegyzes="")
                if szemely.meglevo(self._szemely_kon):
                    print("{} már meglévő személy.". format(szemely))
                else:
                    szemely_id = szemely.ment(self._szemely_kon)
                    # telefonszám
                    telefon = Telefon(szemely=szemely_id, telefonszam=projekt.telefonszam, megjegyzes="")
                    email = Email(szemely=szemely_id, emailcim=projekt.emailcim, megjegyzes="")
                    if telefon.meglevo(self._szemely_kon) or email.meglevo(self._szemely_kon):
                        print("{} már meglévő telefonszám/email-cím.".format(telefon))
                    else:
                        telefon.ment(self._szemely_kon)
                        email.ment(self._szemely_kon)
                # szervezetek
                szervezet = Szervezet(rovidnev=projekt.szervezet, teljesnev="", megjegyzes="", gyakorisag=0)
                szervezet_id = szervezet.ment(self._szervezet_kon) if bool(szervezet) else Kulcs.MAGANSZEMELY.kulcs
                # kontakt
                if szemely_id:
                    kontakt = Kontakt(szemely=szemely_id, szervezet=szervezet_id, megjegyzes="")
                    if not kontakt.meglevo(self._kontakt_kon):
                        kontakt_id = kontakt.ment(self._kontakt_kon)
                # projekt
                ev, szam = projekt.szam.split("/")
                projekt_ = Projekt(ev=ev, szam=szam, megnevezes=projekt.nev, rovidnev="", megjegyzes="")
                if bool(projekt_) and not projekt_.meglevo(self._projekt_kon):
                    projekt_id = projekt_.ment(self._projekt_kon)
                # munkarész
                if projekt_id:
                    munkaresz = Munkaresz(projekt=projekt_id, megnevezes="szigetelés", enaplo=1, megjegyzes="")
                    munkaresz_id = munkaresz.ment(self._projekt_kon)
                # ajánlatkérés
                if kontakt_id and munkaresz_id:
                    ajanlatkeres = Ajanlatkeres(munkaresz=munkaresz_id, ajanlatkero=kontakt_id, temafelelos=1, megjegyzes="")
                    if not ajanlatkeres.meglevo(self._ajanlat_kon):
                        ajanlatkeres_id = ajanlatkeres.ment(self._ajanlat_kon)
                # ajanlat
                if ajanlatkeres_id:
                    ajanlat = Ajanlat(ajanlatkeres=ajanlatkeres_id, ajanlatiar=projekt.ar, megjegyzes="")
                    if not ajanlat.meglevo(self._ajanlat_kon):
                        ajanlat.ment(self._ajanlat_kon)
        return True
