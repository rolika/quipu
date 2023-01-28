"""Csomók tesztelése. A cél, hogy önmagukban is működjenek."""


import unittest

from code.csomo.szemely import Szemely


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
        if not mintaszemely.meglevo():
            mintaszemely.azonosito = mintaszemely.ment()
            self.assertTrue(mintaszemely.torol())
        else:
            self.assertTrue(False)