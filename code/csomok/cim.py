from code.csomok.alapcsomo import Csomo


class Cim(Csomo):
    """Cím megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs:
            kontaktazonosito:   kontakt sql primary key
            cim:                kontakt címe
            megjegyzes:         bármilyen megjegyzés. Használható két, egyébként
                                azonos bejegyzés megkülönböztetésére"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:  # űrlap mezőinek törléséhez
            self._adatok = {
                "orszag": "H",
                "megye": "",
                "iranyitoszam": "",
                "helyseg": "",
                "utca": "",
                "hrsz": "",
                "postafiok": "",
                "honlap": "",
                "tipus": "elsődleges",
                "megjegyzes": ""
            }
        self._db = "kontakt"
        self._tabla = "cim"

    def __str__(self):
        return "{orszag}-{irszam} {helyseg}, {utca}".\
            format(self.orszag, self.iranyitoszam, self.helyseg, self.utca)

    def __bool__(self):
        """Egy cím akkor meghatározott, ha legalább a helység adott"""
        return bool(self._adatok["helyseg"])

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, cim):
        """Új cím-osztály alapján módosítja a meglévőt."""
        self._adatok["orszag"] = cim.orszag
        self._adatok["iranyitoszam"] = cim.iranyitoszam
        self._adatok["megye"] = cim.megye
        self._adatok["helyseg"] = cim.helyseg
        self._adatok["utca"] = cim.utca
        self._adatok["hrsz"] = cim.hrsz
        self._adatok["postafiok"] = cim.postafiok
        self._adatok["honlap"] = cim.honlap
        self._adatok["tipus"] = cim.tipus
        self._adatok["megjegyzes"] = cim.megjegyzes

    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @szemely.setter
    def szemely(self, szemely):
        self._adatok["szemely"] = szemely

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")

    @szervezet.setter
    def szervezet(self, szervezet):
        self._adatok["szervezet"] = szervezet

    @property
    def munkaresz(self):
        return self._adatok.get("munkaresz")
    
    @munkaresz.setter
    def munkaresz(self, munkaresz):
        self._adatok["munkaresz"] = munkaresz

    @property
    def orszag(self):
        return self._adatok.get("orszag", "")
    
    @property
    def megye(self):
        return self._adatok.get("megye", "")

    @property
    def iranyitoszam(self):
        return self._adatok.get("iranyitoszam", "")

    @property
    def helyseg(self):
        return self._adatok.get("helyseg", "")

    @property
    def utca(self):
        return self._adatok.get("utca", "")

    @property
    def hrsz(self):
        return self._adatok.get("hrsz", "")

    @property
    def postafiok(self):
        return self._adatok.get("postafiok", "")

    @property
    def honlap(self):
        return self._adatok.get("honlap", "")

    @property
    def tipus(self):
        return self._adatok.get("tipus", "")

    def listanezet(self):
        return str(self)


if __name__ == "__main__":
    print(Cim().adatok)
