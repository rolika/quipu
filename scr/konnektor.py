"""Adatbázis file-ok létrehozása, megnyitása"""


import pathlib
import json
import tamer


class Konnektor(dict):
    """Adatbázis kapcsolat gyűjtőosztálya.
    Ha még nem léteznek, létrehozza az adatbázis file-okat.
    A külső használat úgy fog kinézni, hogy kon["projekt"].execute(...)"""
    def __init__(self) -> None:
        """Konnektor inicializása."""
        db_path = pathlib.Path("db/")

        with open(pathlib.Path("dat/sql_create.json")) as f:
            self._db_struktura = json.load(f)
        with open(pathlib.Path("dat/sql_default.json")) as f:
            default = json.load(f)

        for db_nev in self._db_struktura:
            for tabla in self._db_struktura[db_nev]:
                self._db_struktura[db_nev][tabla].update(default)

        for db_nev in self._db_struktura:
            print("Kapcsolódás adatbázishoz:", db_nev)
            self[db_nev] = tamer.Tamer(db_path / (db_nev+".db"))
            if db_nev in ("projekt", "raktar"):
                kontakt_kapcsolt = self[db_nev].attach(kontakt=str(db_path / "kontakt.db"))
            else:
                kontakt_kapcsolt = False
            for tabla, oszlopok in self._db_struktura[db_nev].items():
                self._db_struktura[db_nev][tabla]
                self[db_nev].create(tabla, **oszlopok)
            if kontakt_kapcsolt:
                self[db_nev].detach("kontakt")

    @property
    def db_struktura(self):
        return self._db_struktura


#tesztelés
if __name__ == "__main__":
    kon = Konnektor()
    print(kon["projekt"].get_columns("projekt"))