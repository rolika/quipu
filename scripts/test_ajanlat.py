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
                ajanlatkeres_id = None

                # projekt
                ev, szam = projekt.szam.split("/")
                projekt_ = Projekt(ev=ev, szam=szam, megnevezes=projekt.nev, rovidnev="", megjegyzes="", gyakorisag=0)
                if bool(projekt_) and not projekt_.meglevo(self._projekt_kon):
                    projekt_id = projekt_.ment(self._projekt_kon)
                    munkaresz = Munkaresz(projekt=projekt_id, megnevezes="szigetelés", enaplo=1, megjegyzes="")
                    munkaresz_id = munkaresz.ment(self._projekt_kon)
                    orszag = "D" if projekt.orszag == "DE" else "HU"
                    helyseg = projekt.helyseg if projekt.helyseg else "Herend"
                    cim = Cim(munkaresz=munkaresz_id, orszag=orszag, megye="", iranyitoszam="", helyseg=helyseg, utca="", hrsz="", postafiok="", honlap="", megjegyzes="")
                    cim.ment(self._projekt_kon)
                    jelleg = Jelleg(munkaresz=munkaresz_id, megnevezes="új", megjegyzes="")
                    jelleg.ment(self._projekt_kon)

                    # ajánlatkérő szervezet
                    szervezet = Szervezet(rovidnev=projekt.szervezet, teljesnev=projekt.szervezet, gyakorisag=0, megjegyzes=0)
                    if bool(szervezet) and not szervezet.meglevo(self._szervezet_kon):
                        szervezet_id = szervezet.ment(self._szervezet_kon)
                    if not bool(szervezet):
                        szervezet_id = Kulcs.MAGANSZEMELY.kulcs

                    # ajánlatkérő személy
                    nev = projekt.nev.split(" ", maxsplit=1)
                    if len(nev) == 2:
                        vezeteknev, keresztnev = nev
                    elif len(nev) == 1:
                        vezeteknev, keresztnev = nev[0], ""
                    else:
                        vezeteknev, keresztnev = ("Weisz", "Roland")
                    szemely = Szemely(elotag="", vezeteknev=vezeteknev, keresztnev=keresztnev, nem="férfi", megjegyzes="")
                    if not szemely.meglevo(self._szemely_kon):  # a fenti névmanipuláció miatt mindenképpen érvényes lesz
                        szemely_id = szemely.ment(self._szemely_kon)
                        telefonszam = projekt.telefonszam if projekt.telefonszam else "+36"
                        telefon = Telefon(szemely=szemely_id, telefonszam=telefonszam, megjegyzes="")
                        telefon.ment(self._szemely_kon)
                        emailcim = projekt.emailcim if projekt.emailcim else ".hu"
                        email = Email(szemely=szemely_id, emailcim=emailcim, megjegyzes="")
                        email.ment(self._szemely_kon)

                    # kontaktszemély
                    if szervezet_id and szemely_id:
                        kontakt = Kontakt(szemely=szemely_id, szervezet=szervezet_id, beosztas="műszaki előkészítő", gyakorisag=0, megjegyzes="")
                        if not kontakt.meglevo(self._kontakt_kon):
                            kontakt_id = kontakt.ment(self._kontakt_kon)

                    # ajánlatkérés
                    if kontakt_id and munkaresz_id:
                        ajanlatkeres = Ajanlatkeres(munkaresz=munkaresz_id, ajanlatkero=kontakt_id, temafelelos=1, erkezett="", hatarido="", megjegyzes="")
                        if not ajanlatkeres.meglevo(self._ajanlat_kon):
                            ajanlatkeres_id = ajanlatkeres.ment(self._ajanlat_kon)

                    # ajánlat
                    if ajanlatkeres_id:
                        esely = projekt.esely.replace("%", "")
                        try:
                            esely = float(esely) / 100
                        except ValueError:
                            esely = 0.05
                        ajanlat = Ajanlat(ajanlatkeres=ajanlatkeres_id, ajanlatiar=projekt.ar, leadva="", ervenyes="", esely=esely, megjegyzes="")
                        if not ajanlat.meglevo(self._ajanlat_kon):
                            ajanlat.ment(self._ajanlat_kon)


                """ # személyek
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
                        ajanlat.ment(self._ajanlat_kon) """

        return True