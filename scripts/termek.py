from csomo import Csomo
from szervezet import Szervezet
from konstans import TermekTipus


class Termek(Csomo):
    """Termék megvalósítása."""
    def __init__(self, **kwargs) -> object:
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {  # űrlap alaphelyzetbe állítására
                "cikkszam": "",
                "nev": "",
                "tipus" : TermekTipus.SZIG,
                "leiras": "",
                "szin": "",
                "szinkod": "",
                "egyseg": "",
                "kiszereles_nev": "",
                "kiszereles": 0,
                "csomagolas_nev": "",
                "csomagolas": 0,
                "kritikus": 0,
                "szallitasi_ido": 0,
                "megjegyzes": ""
            }
        self._tabla = "termek"

    def __str__(self) -> str:
        return self.listanezet()

    def __repr__(self) -> str:
        return self._ascii_rep("{gyarto}{nev}".format(gyarto=self._gyarto().listanezet(), nev=self.nev))

    def __bool__(self) -> bool:
        """A termék meghatározott, ha van neve és egysége."""
        return bool(self.nev) and bool(self.egyseg)

    @property
    def adatok(self) -> dict:
        return self._adatok

    @adatok.setter
    def adatok(self, termek) -> None:
        self._adatok["cikkszam"] = termek.cikkszam
        self._adatok["nev"] = termek.nev
        self._adatok["tipus"] = termek.tipus
        self._adatok["leiras"] = termek.leiras
        self._adatok["szin"] = termek.szin
        self._adatok["szinkod"] = termek.szinkod
        self._adatok["egyseg"] = termek.egyseg
        self._adatok["kiszereles_nev"] = termek.kiszereles_nev
        self._adatok["kiszereles"] = termek.kiszereles
        self._adatok["csomagolas_nev"] =termek.csomagolas_nev
        self._adatok["csomagolas"] = termek.csomagolas
        self._adatok["kritikus"] = termek.kritikus
        self._adatok["szallitasi_ido"] = termek.szallitasi_ido
        self._adatok["megjegyzes"] = termek.megjegyzes

    @property
    def gyarto(self):
        return self._adatok["gyarto"]

    @gyarto.setter
    def gyarto(self, gyarto):
        self._adatok["gyarto"] = gyarto

    @property
    def cikkszam(self):
        return self._adatok["cikkszam"]

    @property
    def nev(self):
        return self._adatok["nev"]

    @property
    def tipus(self):
        return self._adatok["tipus"]

    @property
    def leiras(self):
        return self._adatok["leiras"]

    @property
    def szin(self):
        return self._adatok["szin"]

    @property
    def szinkod(self):
        return self._adatok["szinkod"]

    @property
    def egyseg(self):
        return self._adatok["egyseg"]

    @property
    def kiszereles_nev(self):
        return self._adatok["kiszereles_nev"]

    @property
    def kiszereles(self):
        return self._adatok["kiszereles"]

    @property
    def csomagolas_nev(self):
        return self._adatok["csomagolas_nev"]

    @property
    def csomagolas(self):
        return self._adatok["csomagolas"]

    @property
    def kritikus(self):
        return self._adatok["kritikus"]

    @property
    def szallitasi_ido(self):
        return self._adatok["szallitasi_ido"]

    def _gyarto(self) -> Szervezet:
        assert self._kon
        gyarto = self._kon.szervezet.select("szervezet", azonosito=self.gyarto).fetchone()
        return Szervezet(kon=self._kon, **gyarto)

    def listanezet(self):
        return "{gyarto} {nev}".format(gyarto=self._gyarto().listanezet(), nev=self.nev)
