from csomo import Csomo
from szervezet import Szervezet
from konstans import AnyagTipus


class Anyag(Csomo):
    """Anyag megvalósítása."""
    tabla = "anyag"

    def __init__(self, **kwargs) -> object:
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {  # űrlap alaphelyzetbe állítására
                "cikkszam": "",
                "nev": "",
                "tipus" : AnyagTipus.SZIG.value,
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
                "eltarthato": 0,
                "megjegyzes": ""
            }
        self._tabla = Anyag.tabla

    def __str__(self) -> str:
        return self.listanezet()

    def __repr__(self) -> str:
        return self._ascii_rep("{gyarto}{nev}".format(gyarto=self._gyarto().listanezet(), nev=self.nev))

    def __bool__(self) -> bool:
        """Az anyag meghatározott, ha van neve és egysége."""
        return bool(self.nev) and bool(self.egyseg)
    
    @classmethod
    def adatbazisbol(cls, kon, azonosito):
        anyag = kon.raktar.select(cls.tabla, azonosito=azonosito).fetchone()
        return cls(kon=kon, **anyag)

    @property
    def adatok(self) -> dict:
        return self._adatok

    @adatok.setter
    def adatok(self, anyag) -> None:
        self._adatok["gyarto"] = anyag.gyarto
        self._adatok["cikkszam"] = anyag.cikkszam
        self._adatok["nev"] = anyag.nev
        self._adatok["tipus"] = anyag.tipus
        self._adatok["leiras"] = anyag.leiras
        self._adatok["szin"] = anyag.szin
        self._adatok["szinkod"] = anyag.szinkod
        self._adatok["egyseg"] = anyag.egyseg
        self._adatok["kiszereles_nev"] = anyag.kiszereles_nev
        self._adatok["kiszereles"] = anyag.kiszereles
        self._adatok["csomagolas_nev"] =anyag.csomagolas_nev
        self._adatok["csomagolas"] = anyag.csomagolas
        self._adatok["kritikus"] = anyag.kritikus
        self._adatok["szallitasi_ido"] = anyag.szallitasi_ido
        self._adatok["eltarthato"] = anyag.eltarthato
        self._adatok["megjegyzes"] = anyag.megjegyzes

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

    @property
    def eltarthato(self):
        return self._adatok["eltarthato"]

    def _gyarto(self) -> Szervezet:
        assert self._kon
        gyarto = self._kon.szervezet.execute("""
            SELECT szervezet.*
            FROM szervezet, gyarto, kontakt
            ON  gyarto.azonosito = ?
                AND kontakt.azonosito = gyarto.kontakt
                AND szervezet.azonosito = kontakt.szervezet;
        """, (self.gyarto, )).fetchone()
        return Szervezet(kon=self._kon, **gyarto)

    def listanezet(self):
        return "{cikkszam} {gyarto} {nev}".format(cikkszam=self.cikkszam, gyarto=self._gyarto().listanezet(), nev=self.nev)
