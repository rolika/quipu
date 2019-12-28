from tkinter import *
from tkinter.ttk import *


class Szemely(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="személy", **kw)

        self.elotag = StringVar()
        self.vezeteknev = StringVar()
        self.keresztnev = StringVar()
        self.nem = StringVar()
        self.megjegyzes = StringVar()

        Label(self, text="előtag").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.elotag, width=8).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.vezeteknev, width=32)\
            .grid(row=1, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.keresztnev, width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="nem").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="nő", value="nő", variable=self.nem)\
            .grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self.nem)\
            .grid(row=3, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.megjegyzes, width=32)\
            .grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)
    
    def beallit(self, **adatok):
        self.elotag.set(adatok.get("elotag", ""))
        self.vezeteknev.set(adatok.get("vezeteknev", ""))
        self.keresztnev.set(adatok.get("keresztnev", ""))
        self.nem.set(adatok.get("nem", "férfi"))
        self.megjegyzes.set(adatok.get("megjegyzes", ""))
    
    def export(self):
        return {"elotag": self.elotag.get(),
                "vezeteknev": self.vezeteknev.get(),
                "keresztnev": self.keresztnev.get(),
                "nem": self.nem.get(),
                "megjegyzes": self.megjegyzes.get()}


class Telefon(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="telefon", **kw)

        self.mezo = {
            "telefonszam": StringVar(),
            "megjegyzes": StringVar()
        }

        Label(self, text="telefonszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["telefonszam"], width=32)\
            .grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["megjegyzes"], width=32)\
            .grid(row=1, column=1, sticky=W, padx=2, pady=2)


class Email(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="email", **kw)

        self.mezo = {
            "emailcim": StringVar(),
            "megjegyzes": StringVar()
        }

        Label(self, text="email-cím").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["emailcim"], width=32)\
            .grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["megjegyzes"], width=32)\
            .grid(row=1, column=1, sticky=W, padx=2, pady=2)


class KezeloGomb(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
    
        self.torles = Button(self, text="törlés", width=8)
        self.reszlet = Button(self, text="részlet", width=8)
        Button(self, text="mégsem", width=8, command=self.quit).grid(row=0, column=2, padx=2, pady=2)
        self.mentes = Button(self, text="mentés", width=8)

        self.torles.grid(row=0, column=0, padx=2, pady=2)
        self.reszlet.grid(row=0, column=1, padx=2, pady=2)
        self.mentes.grid(row=0, column=3, padx=2, pady=2)


class SzemelyUrlap(Frame):
    def __init__(self, master=None, kon=None, azonosito=None, **kw):
        super().__init__(master=master, **kw)

        self.szemely = Szemely()
        self.kezelogomb = KezeloGomb()

        self.szemely.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)
        self.kezelogomb.mentes["command"] = self.ment
        self.kezelogomb.torles["command"] = self.torol
        self.kezelogomb.reszlet["command"] = self.mutat

        self.kon = kon
        self.azonosito = azonosito

        self.szemely.beallit(**self.kivalaszt())
    
    def kivalaszt(self):
        szemely = self.kon.select("szemely", azonosito=self.azonosito)
        return szemely.fetchone() or {}

    def ment(self):
        szemely = self.kivalaszt()
        if szemely:
            if self.kon.update("szemely", self.szemely.export(), azonosito=self.azonosito):
                print("Bejegyzés módosítva.")
        else:
            self.azonosito = self.kon.insert("szemely", **self.szemely.export())
            if self.azonosito:
                print("Új bejegyzés mentve.")
        self.quit()

    def torol(self):
        # TODO: adatbázisban: azonosito INTEGER PRIMARY KEY ON DELETE CASCADE !!!?
        self.kon.delete("telefon", szemely=self.azonosito)
        self.kon.delete("email", szemely=self.azonosito)
        self.kon.delete("cim", szemely=self.azonosito)
        self.kon.delete("kontakt", szemely=self.azonosito)
        if self.kon.delete("szemely", azonosito=self.azonosito):
            print("Bejegyzés törölve.")
        self.quit()
    
    def mutat(self):
        szemely = self.kon.select("elerhetoseg", "elerhetoseg", szemely=self.azonosito)
        szemely = szemely.fetchone()
        if szemely:            
            print(szemely["elerhetoseg"])


if __name__ == "__main__":
    import tamer
    szemelyurlap = SzemelyUrlap(kon = tamer.Tamer("szemely.db"), azonosito=1)
    szemelyurlap.mainloop()
