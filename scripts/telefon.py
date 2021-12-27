from csomo import Csomo


class Telefon(Csomo):
    """Telefonos elérhetőség megvalósítása."""

    tabla = "telefon"

    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        csomo = self.__class__
        super().__init__(kwargs.pop("kon", None), csomo.db, csomo.tabla)
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "telefonszam": "",
                "megjegyzes": ""
            }

    def __str__(self) -> str:
        return self.listanezet()

    def __repr__(self) -> str:
        return Csomo.ascii_rep(self.listanezet())

    def __bool__(self):
        """Telefonszámot kötelező megadni."""
        return bool(self.telefonszam)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, telefon):
        """Új telefon-osztály alapján módosítja a meglévőt."""
        self._adatok["telefonszam"] = telefon.telefonszam
        self._adatok["megjegyzes"] = telefon.megjegyzes

    @property
    def szemely(self):
        return self._adatok.get("szemely")

    @property
    def szervezet(self):
        return self._adatok.get("szervezet")

    @szervezet.setter
    def szervezet(self, szervezet):
        self._adatok["szervezet"] = szervezet

    @szemely.setter
    def szemely(self, szemely):
        self._adatok["szemely"] = szemely

    @property
    def telefonszam(self):
        return self._adatok.get("telefonszam")

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{}{}".format(self.telefonszam, Csomo.formazo(self.megjegyzes))
