"""Csomók tesztelése. A cél, hogy önmagukban is működjenek."""


import unittest

from code.csomo.szemely import Szemely
from code.csomo.szervezet import Szervezet
from code.csomo.kontakt import Kontakt


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