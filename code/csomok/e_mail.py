from .alapcsomo import Csomo


class Email(Csomo):
    """Email-elérhetőség megvalósítása."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs:
            kontaktazonosito:   kontakt sql primary key
            emailcimn:          kontakt email-címe
            megjegyzes:         bármilyen megjegyzés. Használható két, egyébként
                                azonos bejegyzés megkülönböztetésére"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "emailcim": "",
                "tipus": "elsődleges",
                "megjegyzes": ""
            }
        self._db = "kontakt"
        self._tabla = "email"

    def __bool__(self):
        return bool(self.emailcim)

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, email):
        """Új email-osztály alapján módosítja a meglévőt."""
        self._adatok["emailcim"] = email.emailcim
        self._adatok["megjegyzes"] = email.megjegyzes

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
    def emailcim(self):
        return self._adatok.get("emailcim")

    @property
    def tipus(self):
        return self._adatok.get("tipus", "")

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{} ({})".format(self.emailcim, Csomo.formazo(self.megjegyzes))
