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
from e_mail import Email
from szervezet import Szervezet
from kontakt import Kontakt
from projekt import Projekt
from munkaresz import Munkaresz
from ajanlatkeres import Ajanlatkeres
from ajanlat import Ajanlat
from cim import Cim
from jelleg import Jelleg
from konnektor import Konnektor
from konstans import Esely


class ProjektlistaTest(unittest.TestCase):
    """Adatbázis feltöltése projektlistából"""

    def setUp(self) -> None:
        self._kon = Konnektor(szemely=Tamer("szemely.db"),
                              szervezet=Tamer("szervezet.db"),
                              kontakt=Tamer("kontakt.db"),
                              projekt=Tamer("projekt.db"),
                              ajanlat=Tamer("ajanlat.db"))

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
                if bool(projekt_) and not projekt_.meglevo(self._kon.projekt):
                    projekt_id = projekt_.ment(self._kon.projekt)
                    munkaresz = Munkaresz(kon=self._kon, projekt=projekt_id, megnevezes="szigetelés", enaplo=1, megjegyzes="")
                    munkaresz_id = munkaresz.ment(self._kon.projekt)
                    orszag = "D" if projekt.orszag.startswith("D") else "H"
                    helyseg = projekt.helyseg if projekt.helyseg else "Herend"
                    cim = Cim(munkaresz=munkaresz_id, orszag=orszag, megye="", iranyitoszam="", helyseg=helyseg, utca="", hrsz="", postafiok="", honlap="", megjegyzes="alapértelmezett")
                    cim.ment(self._kon.projekt)
                    jelleg = Jelleg(kon=self._kon, munkaresz=munkaresz_id, megnevezes="új", megjegyzes="")
                    jelleg_id = jelleg.ment(self._kon.projekt)

                    # ajánlatkérő szervezet
                    szervezet = Szervezet(rovidnev=projekt.szervezet, teljesnev=projekt.szervezet, gyakorisag=0, megjegyzes="")
                    if not bool(szervezet):
                        szervezet_id = 1  # magánszemély azonosítója
                    else:
                        szervezet.rovidnev = szervezet.rovidnev.split()[0]
                        meglevo = szervezet.meglevo(self._kon.szervezet)  # kezeli a agánszemélyt is, ami mindig meglévő
                        if meglevo:
                            szervezet_id = Szervezet(**meglevo).azonosito
                        else:
                            szervezet_id = szervezet.ment(self._kon.szervezet)

                    # ajánlatkérő személy
                    nev = projekt.szemely.split(" ", maxsplit=1)
                    if len(nev) == 2:
                        vezeteknev, keresztnev = nev
                    elif len(nev) == 1:
                        vezeteknev, keresztnev = nev[0], ""
                    szemely = Szemely(elotag="", vezeteknev=vezeteknev, keresztnev=keresztnev, nem="férfi", megjegyzes="")
                    if bool(szemely) and not szemely.meglevo(self._kon.szemely):
                        szemely_id = szemely.ment(self._kon.szemely)
                        telefonszam = projekt.telefonszam if projekt.telefonszam else "+36"
                        telefon = Telefon(szemely=szemely_id, telefonszam=telefonszam, megjegyzes="alapértelmezett")
                        telefon.ment(self._kon.szemely)
                        emailcim = projekt.emailcim if projekt.emailcim else ".hu"
                        email = Email(szemely=szemely_id, emailcim=emailcim, megjegyzes="alapértelmezett")
                        email.ment(self._kon.szemely)

                    # kontaktszemély
                    if szervezet_id and szemely_id:
                        kontakt = Kontakt(kon=self._kon, szemely=szemely_id, szervezet=szervezet_id, gyakorisag=0, megjegyzes="")
                        if not kontakt.meglevo(self._kon.kontakt):
                            kontakt_id = kontakt.ment(self._kon.kontakt)

                    # ajánlatkérés
                    if kontakt_id and jelleg_id:
                        ajanlatkeres = Ajanlatkeres(kon=self._kon, jelleg=jelleg_id, ajanlatkero=kontakt_id, temafelelos=1)
                        if not ajanlatkeres.meglevo(self._kon.ajanlat):
                            ajanlatkeres_id = ajanlatkeres.ment(self._kon.ajanlat)

                    # ajánlat
                    if ajanlatkeres_id and projekt.ar and int(projekt.ar) > 0:  # ár nélkül nem írom be az ajánlatok közé
                        esely = projekt.esely.rstrip("%")
                        try:
                            esely = int(esely)
                        except ValueError:
                            esely = Esely.NORMAL
                        ajanlat = Ajanlat(kon=self._kon, ajanlatkeres=ajanlatkeres_id, ajanlatiar=projekt.ar, leadva="", ervenyes="", esely=esely, megjegyzes="")
                        if not ajanlat.meglevo(self._kon.ajanlat):
                            ajanlat.ment(self._kon.ajanlat)

        return True

if __name__ == "__main__":
    ProjektlistaTest()