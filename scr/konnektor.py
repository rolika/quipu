"""Adatbázis file-ok létrehozása, megnyitása"""

import pathlib
import json
import tamer


class Konnektor:
    """Adatbázis kapcsolat gyűjtőosztálya.
    Ha még nem léteznek, létrehozza az adatbázis file-okat.
    A külső használat úgy fog kinézni, hogy pl. kon.projekt.select(...)"""
    def __init__(self, **kwargs) -> None:
        """Konnektor inicializása.
        kwargs: név=konnektor párosok
            A név egy valid Python változó legyen, ami célszerűen azonos az adatbázis filenevekkel.
            A konnektor pedig az adatbázis-file csatlakozásánák hivatkozása.
        """
        db_path = pathlib.Path("db/")
        self._kon = dict()

        with open(pathlib.Path("sql/sql_create.json")) as f:
            self._db_struktura = json.load(f)
        with open(pathlib.Path("sql/sql_default.json")) as f:
            default = json.load(f)
        
        for db_nev in self._db_struktura:
            for tabla in self._db_struktura[db_nev]:
                self._db_struktura[db_nev][tabla].update(default)
        
        for db_nev in self._db_struktura:
            print("Kapcsolódás adatbázishoz:", db_nev)
            self._kon[db_nev] = tamer.Tamer(db_path / (db_nev+".db"))
            if db_nev in ("projekt", "raktar"):
                kontakt_kapcsolt = self._kon[db_nev].attach(kontakt=str(db_path / "kontakt.db"))
            else:
                kontakt_kapcsolt = False
            for tabla, oszlopok in self._db_struktura[db_nev].items():
                self._db_struktura[db_nev][tabla]
                self._kon[db_nev].create(tabla, **oszlopok)
            if kontakt_kapcsolt:
                self._kon[db_nev].detach("kontakt")
    
    @property
    def db_struktura(self):
        return self._db_struktura
    
    def szemelyhez_rendelt_szervezetek(self, szemelyazonosito):
        self._kon.szemely.execute("""
            SELECT *
            FROM szervezet
            WHERE azonosito IN (
                SELECT szervezet
                FROM kontakt
                WHERE szemely = ?
            );
        """, (szemelyazonosito, ))


# az elv tesztelése
if __name__ == "__main__":
    kon = Konnektor()