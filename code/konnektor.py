"""Adatbázis file-ok létrehozása, megnyitása"""


import pathlib
import json
from code.tamer import Tamer


class Konnektor(dict):
    """Adatbázis kapcsolat gyűjtőosztálya.
    Ha még nem léteznek, létrehozza az adatbázis file-okat.
    A külső használat úgy fog kinézni, hogy kon["db"]["tabla"].execute(...)"""
    def __init__(self) -> None:
        """Konnektor inicializása."""
        super().__init__()
        db_path = pathlib.Path("data/db/")

        with open(pathlib.Path("data/sql_create.json")) as f:
            self._db_struktura = json.load(f)
        with open(pathlib.Path("data/sql_default.json")) as f:
            self._alapertelmezett_oszlopok = json.load(f)

        for db_nev in self._db_struktura:
            print("Kapcsolódás adatbázishoz:", db_nev)
            self[db_nev] = Tamer(db_path / (db_nev+".db"))
            for tabla, oszlop in self._db_struktura[db_nev].items():
                if tabla != "_attach_":
                    oszlop.update(self._alapertelmezett_oszlopok)
                    self[db_nev].create(tabla, **oszlop)

    @property
    def alap_oszlopok(self):
        alap = dict(self._alapertelmezett_oszlopok)
        del alap["megjegyzes"]  # elvileg ez nem tud KeyError-t dobni
        return alap.keys()

#tesztelés
if __name__ == "__main__":
    kon = Konnektor()
    print(kon["projekt"].get_columns("projekt"))