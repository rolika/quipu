from .alapcsomo import Csomo


class Telefon(Csomo):
    """Telefonos elérhetőség megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs:
            kontaktazonosito:   kontakt sql primary key
            telefonszam:        kontakt telefonszáma
            megjegyzes:         bármilyen megjegyzés. Használható két, egyébként
                                azonos bejegyzés megkülönböztetésére"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "telefonszam": "",
                "tipus": "elsődleges",
                "megjegyzes": ""
            }
        self._db = "kontakt"
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

    @property
    def tipus(self):
        return self._adatok.get("tipus", "")

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{}{}".format(self.telefonszam, Csomo.formazo(self.megjegyzes))
