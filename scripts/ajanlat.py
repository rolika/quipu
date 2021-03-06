import dolog


class Ajanlat(dolog.Dolog):
    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self._adatok = dict(kwargs)
        else:
            self._adatok = {
                "ajanlatiar": "",
                "ervenyes": "",
                "esely": "",
                "megjegyzes": ""
            }
        self._tabla = "ajanlat"

    def __bool__(self):
        return True

    @property
    def adatok(self):
        return self._adatok

    @adatok.setter
    def adatok(self, ajanlat):
        self._adatok["ajanlatkeres"] = ajanlat.ajanlatkeres
        self._adatok["ajanlatiar"] = ajanlat.ajanlatiar
        self._adatok["leadva"] = ajanlat.leadva
        self._adatok["ervenyes"] = ajanlat.ervenyes
        self._adatok["esely"] = ajanlat.esely
        self._adatok["megjegyzes"] = ajanlat.megjegyzes

    @property
    def ajanlatkeres(self):
        return self._adatok.get("ajanlatkeres")
    
    @ajanlatkeres.setter
    def ajanlatkeres(self, ajker):
        self._adatok["ajanlatkeres"] = ajker

    @property
    def ajanlatiar(self):
        return self._adatok.get("ajanlatiar")

    @property
    def leadva(self):
        return self._adatok.get("leadva")

    @property
    def ervenyes(self):
        return self._adatok.get("ervenyes")

    @property
    def esely(self):
        return self._adatok.get("esely")