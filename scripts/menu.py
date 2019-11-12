from collections import namedtuple


class Menu:
    """
    Az osztály feladata egy számozott menü megjelenítése a konzolon.
    Ha nincs szülője (azaz főmenü), akkor automatikusan hozzáadja a kilépés menüpontot.
    Ha van szülője (azaz almenü), akkor hozzáadja a vissza (visszalép a szülő-menübe) és főmenü pontokat.
    """
    def __init__(self, *menupontok, szulo=None):
        """
        Előkészíti a menüpontokat, kiegészíti az alapértelmezett elemekkel.
        menupontok: ("menüpont szövege", kezelőfüggvény referenciája) tuple-k sorozata
        szulo:      főmenü esetén None, almenü esetén a szülőosztály példánya
        """
        Menupont = namedtuple("Menupont", "szoveg kezelo")
        menupontok = list(menupontok)
        if szulo:
            menupontok.append(("vissza", szulo.prompt))
            menupontok.append(("főmenü", None))
        else:
            menupontok.append(("kilépés", quit))
        self.menupontok = tuple(map(Menupont._make, menupontok))
        self.szulo = szulo

    def prompt(self):
        """
        Kiírja konzolra a menüpontokat (kiegészítve az alapértelmezett elemekkel),
        bekéri felhasználó választását, ellenőrzi a helyességét,
        visszatér a meghívandó függvény referenciájával.
        """
        for i, menupont in enumerate(self.menupontok):
            print("{:2}. {}".format(i+1, menupont.szoveg))
        while True:
            valasztas = input("> ")
            try:
                valasztas = int(valasztas)
                if valasztas not in range(1, len(self.menupontok)+1):
                    raise ValueError
                break
            except ValueError:
                print("Kérem, hogy a fenti számok közül válassz!")
        return self.menupontok[valasztas-1].kezelo


if __name__ == "__main__":
    menu = Menu(
        ("választási lehetőség 1", lambda mp: print("1. menüpont")),
        ("választási lehetőség 2", lambda mp: print("2. menüpont")),
        szulo=None)
    almenu = Menu(
        ("almenü 1.", lambda mp: print("1. almenüpont")),
        ("almenü 2.", lambda mp: print("2. almenüpont")),
        szulo=menu)
    almenu.prompt()()  # a lambdáknak kell legalább egy None argumentum a második zárójelbe
