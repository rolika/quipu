from csomo import Csomo


class Telefon(Csomo):
    """Telefonos elérhetőség megvalósítása. Egyszerű csomó, egy külső kulcsra támaszkodik."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "telefonszam": "",
                "megjegyzes": ""
            }
        self._tabla = "telefon"

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
        return "{}{}".format(self.telefonszam, self._nullazo(self.megjegyzes))
