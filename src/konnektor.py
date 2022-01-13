class Konnektor(dict):
    """Adatbázis kapcsolat gyűjtőosztálya.
    A vég nélküli paraméterlistákat hivatott kiváltani, egy név alá gyűjtve az összes adatbázis-kapcsolatot.
    Kezeli az összetett lekérdezéseket, melyeket a tamer.Tamer() nem tud."""
    def __init__(self, **kwargs) -> None:
        """Konnektor inicializása.
        kwargs: név=konnektor párosok
            A név egy valid Python változó legyen, ami célszerűen azonos az adatbázis filenevekkel.
            A konnektor pedig az adatbázis-file csatlakozásánák hivatkozása.

        A külső használat úgy fog kinézni, hogy pl. kon.projekt.select(...)
        """
        super().__init__(**kwargs)
        for nev, kon in kwargs.items():
            setattr(self, nev, kon)

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
    kon = Konnektor(szemely="ez lesz a személykonnektor",
                    szervezet="ő pedig a szervezet-konnektor",
                    projekt="a projektek konnektora")
    print(kon.szemely)
    print(kon.szervezet)
    print(kon.projekt)
    print("###############################")
    print(kon["szemely"])
    print(kon["szervezet"])
    print(kon["projekt"])