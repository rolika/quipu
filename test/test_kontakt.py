"""Csomók tesztelése. A cél, hogy önmagukban is működjenek.
Az adatbázis file-ok is változatlanok maradnak."""


import unittest

from code.csomok.szemely import Szemely
from code.csomok.szervezet import Szervezet
from code.csomok.kontakt import Kontakt
from code.csomok.telefon import Telefon
from code.csomok.e_mail import Email
from code.csomok.cim import Cim


class CsomoTest(unittest.TestCase):
    def setUp(self) -> None:
        self._mintaszemely = Szemely(elotag="Dr.",
                                     vezeteknev="Minta",
                                     keresztnev="Aladár",
                                     becenev="Alibá",
                                     nem="férfi",
                                     megjegyzes="bácsi")
        self._mintaceg = Szervezet(rovidnev="Cég Kft.",
                                   teljesnev="Cég Ipari és Szolgáltató Kft.")
        self._mintaszemely.azonosito = self._mintaszemely.ment()
        self._mintaceg.azonosito = self._mintaceg.ment()

        self._kontakt = Kontakt(szemelyazonosito=self._mintaszemely.azonosito,
                          szervezetazonosito=self._mintaceg.azonosito)
        self._kontakt.azonosito = self._kontakt.ment()

        self._telefon = Telefon(kontaktazonosito=self._kontakt.azonosito,
                          telefonszam="+56-42-565 88 99")
        self._email = Email(kontaktazonosito=self._kontakt.azonosito,
                      emailcim="drminta@ceg.hu")
        self._cim = Cim(kontaktazonosito=self._kontakt.azonosito,
                  megye="BAZ",
                  iranyitoszam="3245",
                  helyseg="Város",
                  kozterulet="Fiktiv u. 1.",
                  hrsz="32/23",
                  postafiok="10",
                  honlap="www.ceg.hu",
                  megjegyzes="nahát")

        self._telefon.azonosito = self._telefon.ment()
        self._email.azonosito = self._email.ment()
        self._cim.azonosito = self._cim.ment()

    def test_kontakt(self):
        becenev = Szemely.azonositobol\
            ("kontakt", "szemely", self._mintaszemely.azonosito).becenev
        cegnev = Szervezet.azonositobol\
            ("kontakt", "szervezet", self._mintaceg.azonosito).rovidnev
        telefonszam = Telefon.azonositobol\
            ("kontakt", "telefon", self._telefon.azonosito).telefonszam
        emailcim = Email.azonositobol\
            ("kontakt", "email", self._email.azonosito).emailcim
        irszam = Cim.azonositobol("kontakt", "cim", self._cim.azonosito).iranyitoszam

        self.assertEqual(becenev+cegnev+telefonszam+emailcim+irszam,
                         "AlibáCég Kft.+56-42-565 88 99drminta@ceg.hu3245")
    
    def tearDown(self) -> None:
        self._mintaszemely.torol()
        self._mintaceg.torol()
        self._kontakt.torol()
        self._telefon.torol()
        self._email.torol()
        self._cim.torol()