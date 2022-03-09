"""Adatbázis file-ok létrehozása, megnyitása"""

import pathlib
import json
import tamer


class Konnektor:
    """Adatbázis kapcsolat gyűjtőosztálya.
    A külső használat úgy fog kinézni, hogy pl. kon.projekt.select(...)"""
    def __init__(self, **kwargs) -> None:
        """Konnektor inicializása.
        kwargs: név=konnektor párosok
            A név egy valid Python változó legyen, ami célszerűen azonos az adatbázis filenevekkel.
            A konnektor pedig az adatbázis-file csatlakozásánák hivatkozása.
        """
        db_path = pathlib.Path("db/").resolve()
        self._kon = dict()

        # ha még nem léteznek, létrehozom az adatbázis file-okat
        with open(pathlib.Path("sql/sql_create.json")) as f:
            self._db_struktura = json.load(f)
        
        for db_nev in self._db_struktura:
            print("Kapcsolódás adatbázishoz:", db_nev)
            self._kon[db_nev] = tamer.Tamer(db_path / (db_nev+".db"))
            if db_nev in ("projekt", "raktar"):
                kontakt_kapcsolt = self._kon[db_nev].attach(kontakt=str(db_path/"kontakt.db"))
            else:
                kontakt_kapcsolt = False
            for tabla, oszlopok in self._db_struktura[db_nev].items():
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