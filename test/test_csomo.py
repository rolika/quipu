"""Csomók tesztelése. A cél, hogy önmagukban is működjenek.
Az adatbázis file-ok is változatlanok maradnak."""


import unittest
import sys

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

    def test_szemely(self):
        if not self._mintaszemely.meglevo():  # működik-e a meglévő, ha igen
            self._mintaszemely.azonosito = self._mintaszemely.ment()  # mentés,
            self.assertTrue(self._mintaszemely.torol())  # majd törlés
        else:
            self.assertTrue(False)  # amúgy valami nem volt jó

    def test_szervezet(self):
        if not self._mintaceg.meglevo():
            self._mintaceg.azonosito = self._mintaceg.ment()
            self.assertTrue(self._mintaceg.torol())
        else:
            self.assertTrue(False)

    def test_kontakt(self):
        self._mintaszemely.azonosito = self._mintaszemely.ment()
        self._mintaceg.azonosito = self._mintaceg.ment()

        kontakt = Kontakt(szemelyazonosito=self._mintaszemely.azonosito,
                          szervezetazonosito=self._mintaceg.azonosito)
        kontakt.azonosito = kontakt.ment()

        self._mintaszemely.torol()
        self._mintaceg.torol()
        self.assertTrue(kontakt.torol())

    def test_elerhetoseg(self):
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

        self._mintaszemely.torol()
        self._mintaceg.torol()
        kontakt.torol()

        self.assertTrue(telefon.torol() and email.torol() and cim.torol())