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
from cim import Cim
from jelleg import Jelleg
from konstans import MAGANSZEMELY, ROLI


class ProjektlistaTest(unittest.TestCase):
    """Adatbázis feltöltése projektlistából"""

    def setUp(self) -> None:
        self._szemely_kon = Tamer("szemely.db")
        self._szervezet_kon = Tamer("szervezet.db")
        self._kontakt_kon = Tamer("kontakt.db")
        self._projekt_kon = Tamer("projekt.db")
        self._ajanlat_kon = Tamer("ajanlat.db")

    def test_projektlista_import(self):
        ProjektRekord = namedtuple("ProjektRekord", ["szam", "nev", "helyseg", "orszag", "ev", "ar", "euro", "felulet",
            "esely", "statusz", "temafelelos", "szervezet", "szemely", "telefonszam", "emailcim", "hoszig", "mm",
            "szig", "m2ar", "eurom2ar"])

        with open("projektlista.csv", newline='') as projektek:
            for projekt in map(ProjektRekord._make, csv.reader(projektek, delimiter=";")):
                projekt_id = None
                szemely_id = None
                szervezet_id = None
                kontakt_id = None
                munkaresz_id = None
                jelleg_id = None
                ajanlatkeres_id = None

                # projekt
                ev, szam = projekt.szam.split("/")
                projekt_ = Projekt(ev=ev, szam=szam, megnevezes=projekt.nev, rovidnev="", megjegyzes="", gyakorisag=0)
                if bool(projekt_) and not projekt_.meglevo(self._projekt_kon):
                    projekt_id = projekt_.ment(self._projekt_kon)
                    munkaresz = Munkaresz(projekt=projekt_id, megnevezes="szigetelés", enaplo=1, megjegyzes="")
                    munkaresz_id = munkaresz.ment(self._projekt_kon)
                    orszag = "D" if projekt.orszag.startswith("D") else "H"
                    helyseg = projekt.helyseg if projekt.helyseg else "Herend"
                    cim = Cim(munkaresz=munkaresz_id, orszag=orszag, megye="", iranyitoszam="", helyseg=helyseg, utca="", hrsz="", postafiok="", honlap="", megjegyzes="")
                    cim.ment(self._projekt_kon)
                    jelleg = Jelleg(munkaresz=munkaresz_id, megnevezes="új", megjegyzes="")
                    jelleg_id = jelleg.ment(self._projekt_kon)

                    # ajánlatkérő szervezet
                    szervezet = Szervezet(rovidnev=projekt.szervezet, teljesnev=projekt.szervezet, gyakorisag=0, megjegyzes="")
                    if not bool(szervezet):  # ha nincs szervezet feltüntve, akkor magánszemély
                        szervezet_id = MAGANSZEMELY.azonosito
                    else:
                        meglevo = szervezet.meglevo(self._szervezet_kon)
                        if meglevo:
                            szervezet_id = Szervezet(**meglevo).azonosito
                        else:
                            szervezet_id = szervezet.ment(self._szervezet_kon)

                    # ajánlatkérő személy
                    nev = projekt.szemely.split(" ", maxsplit=1)
                    if len(nev) == 2:
                        vezeteknev, keresztnev = nev
                    elif len(nev) == 1:
                        vezeteknev, keresztnev = nev[0], ""
                    szemely = Szemely(elotag="", vezeteknev=vezeteknev, keresztnev=keresztnev, nem="férfi", megjegyzes="")
                    if bool(szemely) and not szemely.meglevo(self._szemely_kon):
                        szemely_id = szemely.ment(self._szemely_kon)
                        telefonszam = projekt.telefonszam if projekt.telefonszam else "+36"
                        telefon = Telefon(szemely=szemely_id, telefonszam=telefonszam, megjegyzes="")
                        telefon.ment(self._szemely_kon)
                        emailcim = projekt.emailcim if projekt.emailcim else ".hu"
                        email = Email(szemely=szemely_id, emailcim=emailcim, megjegyzes="")
                        email.ment(self._szemely_kon)

                    # kontaktszemély
                    if szervezet_id and szemely_id:
                        kontakt = Kontakt(szemely=szemely_id, szervezet=szervezet_id, gyakorisag=0, megjegyzes="")
                        if not kontakt.meglevo(self._kontakt_kon):
                            kontakt_id = kontakt.ment(self._kontakt_kon)

                    # ajánlatkérés
                    if kontakt_id and jelleg_id:
                        ajanlatkeres = Ajanlatkeres(jelleg=jelleg_id, ajanlatkero=kontakt_id, temafelelos=ROLI.azonosito)
                        if not ajanlatkeres.meglevo(self._ajanlat_kon):
                            ajanlatkeres_id = ajanlatkeres.ment(self._ajanlat_kon)

                    # ajánlat
                    if ajanlatkeres_id and projekt.ar and float(projekt.ar) > 0:  # ár nélkül nem írom be az ajánlatok közé
                        esely = projekt.esely.replace("%", "")
                        try:
                            esely = int(esely)
                        except ValueError:
                            esely = 10
                        ajanlat = Ajanlat(ajanlatkeres=ajanlatkeres_id, ajanlatiar=projekt.ar, leadva="", ervenyes="", esely=esely, megjegyzes="")
                        if not ajanlat.meglevo(self._ajanlat_kon):
                            ajanlat.ment(self._ajanlat_kon)

        return True
