from csomo import Csomo


class Email(Csomo):
    """Email-elérhetőség megvalósítása.
    Egyszerű csomó, egy külső kulcsra támaszkodik, ami azonos adatbázis file-ban van."""
    def __init__(self, **kwargs):
        """Konstruktor adatbázisból vagy űrlapból történő példányosításhoz.
        kwargs: adatok kulcs=érték párokként, akár sqlite Row-objektum is (hozzáférés oszlopnevekkel)"""
        super().__init__(kwargs.pop("kon", None))
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "emailcim": "",
                "megjegyzes": ""
            }
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

    def listanezet(self):
        """Elérhetőseg megjelenítése kiválasztáshoz (Combobox)"""
        return "{} ({})".format(self.emailcim, self.megjegyzes)
