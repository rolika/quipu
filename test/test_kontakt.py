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

    def test_kontakt(self):
        self._mintaszemely.azonosito = self._mintaszemely.ment()
        self._mintaceg.azonosito = self._mintaceg.ment()

        kontakt = Kontakt(szemelyazonosito=self._mintaszemely.azonosito,
                          szervezetazonosito=self._mintaceg.azonosito)
        kontakt.azonosito = kontakt.ment()

        telefon = Telefon(kontaktazonosito=kontakt.azonosito,
                          telefonszam="+56-42-565 88 99")
        email = Email(kontaktazonosito=kontakt.azonosito,
                      emailcim="drminta@ceg.hu")
        cim = Cim(kontaktazonosito=kontakt.azonosito,
                  megye="BAZ",
                  iranyitoszam="3245",
                  helyseg="Város",
                  kozterulet="Fiktiv u. 1.",
                  hrsz="32/23",
                  postafiok="10",
                  honlap="www.ceg.hu",
                  megjegyzes="nahát")

        telefon.azonosito = telefon.ment()
        email.azonosito = email.ment()
        cim.azonosito = cim.ment()

        becenev = Szemely.azonositobol\
            ("kontakt", "szemely", self._mintaszemely.azonosito).becenev
        cegnev = Szervezet.azonositobol\
            ("kontakt", "szervezet", self._mintaceg.azonosito).rovidnev
        telefonszam = Telefon.azonositobol\
            ("kontakt", "telefon", telefon.azonosito).telefonszam
        emailcim = Email.azonositobol\
            ("kontakt", "email", email.azonosito).emailcim
        irszam = Cim.azonositobol("kontakt", "cim", cim.azonosito).iranyitoszam

        self._mintaszemely.torol()
        self._mintaceg.torol()
        kontakt.torol()
        telefon.torol()
        email.torol()
        cim.torol()

        self.assertEqual(becenev+cegnev+telefonszam+emailcim+irszam,
                         "AlibáCég Kft.+56-42-565 88 99drminta@ceg.hu3245")