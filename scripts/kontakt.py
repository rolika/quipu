from csomo import Csomo
from konstans import MAGANSZEMELY
from szemely import Szemely
from szervezet import Szervezet


class Kontakt(Csomo):
    """Kontaktszemély megvalósítása. Összetett csomó, több külső kulcsra támaszkodik."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._ceg_elol = kwargs.pop("ceg_elol", True)
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "szemely": 0,
                "szervezet": 0,
                "megjegyzes": ""
            }
            self._ceg_elol = True
        self._tabla = "kontakt"

    def __str__(self) ->str:
        """Szervezeti adatok megjelenítése terminál-nézethez."""
        return "{ceg}{nev}".format(ceg=str(self._szervezet()), nev=self._szemely().listanezet())

    def __repr__(self) -> str:
        """Név megjelenítése sorbarendezéshez"""
        return self._ascii_rep(self.listanezet())

    def __bool__(self) -> bool:
        return True

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, kontakt):
        self._adatok["szemely"] = kontakt.szemely
        self._adatok["szervezet"] = kontakt.szervezet
        self._adatok["megjegyzes"] = kontakt.megjegyzes

    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")

    def _szemely(self) -> Szemely:
        """A kontakt személyi adatai."""
        assert self._kon
        szemely = self._kon.szemely.select("szemely", azonosito=self.szemely).fetchone()
        return Szemely(**szemely)

    def _szervezet(self) -> Szervezet:
        """A kontakt szervezeti adatai."""
        assert self._kon
        szervezet = self._kon.szervezet.select("szervezet", azonosito=self.szervezet).fetchone()
        szervezet = Szervezet(kon=self._kon, **szervezet)
        if szervezet == MAGANSZEMELY:  # __eq__ használata
            szervezet.rovidnev = ""
        return szervezet

    def listanezet(self) -> str:
        """Kontakt szöveges megjelenítése kiválasztáshoz (pl. Combobox)."""
        if self._ceg_elol:
            return "{ceg}{nev}".format(ceg=self._nullazo(self._szervezet().listanezet(),
                                                         zarojel="",
                                                         elvalasztojel=": ",
                                                         hatul=True),
                                       nev=self._szemely().listanezet())
        else:
            return "{nev}{ceg}".format(nev=self._szemely().listanezet(),
                                       ceg=self._nullazo(self._szervezet().listanezet(),
                                                         zarojel="",
                                                         elvalasztojel=" / "))