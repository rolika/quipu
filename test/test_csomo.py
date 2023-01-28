"""Csomók tesztelése. A cél, hogy önmagukban is működjenek."""


import unittest

from code.csomo.szemely import Szemely
from code.csomo.szervezet import Szervezet


class CsomoTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_szemely(self):
        mintaszemely = Szemely(elotag="Dr.",
                               vezeteknev="Minta",
                               keresztnev="Aladár",
                               becenev="Alibá",
                               nem="férfi",
                               megjegyzes="bácsi")
        if not mintaszemely.meglevo():  # működik-e a meglévő, ha igen
            mintaszemely.azonosito = mintaszemely.ment()  # mentés,
            self.assertTrue(mintaszemely.torol())  # majd törlés
        else:
            self.assertTrue(False)  # amúgy valami nem volt jó

    def test_szervezet(self):
        mintaceg = Szervezet(rovidnev="Cég Kft.",
                             teljesnev="Cég Ipari és Szolgáltató Kft.")
        if not mintaceg.meglevo():
            mintaceg.azonosito = mintaceg.ment()
            self.assertTrue(mintaceg.torol())
        else:
            self.assertTrue(False)