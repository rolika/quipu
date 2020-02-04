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
        Radiobutton(self, text="nő", value="nő", variable=self.nem).grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self.nem).grid(row=3, column=2, sticky=W, padx=2, pady=2)

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


class KetMezo(LabelFrame):
    def __init__(self, cimke, mezo1, mezo2, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)

        self.mezo1_oszlop = mezo1[1]
        self.mezo2_oszlop = mezo2[1]
        mezo1 = mezo1[0]
        mezo2 = mezo2[0]

        self.mezo1 = StringVar()
        self.mezo2 = StringVar()

        Label(self, text=mezo1).grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo1, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text=mezo2).grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo2, width=32).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, **adatok):
        self.mezo1.set(adatok.get(self.mezo1_oszlop, ""))
        self.mezo2.set(adatok.get(self.mezo2_oszlop, ""))

    def export(self):
        return {self.mezo1_oszlop: self.mezo1.get(), self.mezo2_oszlop: self.mezo2.get()}


class Valaszto(LabelFrame):
    def __init__(self, text, master=None, **kw):
        super().__init__(master=master, text=text, **kw)

        self.valaszto = Combobox(self, width=32)
        self.valaszto.grid()


class KezeloGomb(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.torles = Button(self, text="törlés", width=8)
        self.reszlet = Button(self, text="részlet", width=8)
        self.megsem = Button(self, text="mégsem", width=8)
        self.mentes = Button(self, text="mentés", width=8)

        self.torles.grid(row=0, column=0, padx=2, pady=2)
        self.reszlet.grid(row=0, column=1, padx=2, pady=2)
        self.megsem.grid(row=0, column=2, padx=2, pady=2)
        self.mentes.grid(row=0, column=3, padx=2, pady=2)


class SzemelyUrlap(Frame):
    def __init__(self, master=None, kon=None, azonosito=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon
        self.azonosito = azonosito

        self.szemely = Szemely(self)
        self.kezelogomb = KezeloGomb(self)

        self.szemely.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)
        self.kezelogomb.mentes["command"] = self.ment
        self.kezelogomb.torles["command"] = self.torol
        self.kezelogomb.reszlet["command"] = self.mutat
        self.kezelogomb.megsem["command"] = master.destroy

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


class TelefonUrlap(Frame):
    def __init__(self, kon, master=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon
        self.azonosito = None

        self.szemely = Valaszto("személyek")
        self.ujtelefon = KetMezo("új telefonszám", ("telefonszám", "telefonszam"), ("megjegyzés", "megjegyzes"))
        self.meglevotelefon = Valaszto("meglévő telefonszámok")
        self.kezelogomb = KezeloGomb()
        self.kezelogomb.mentes["command"] = self.ment
        self.kezelogomb.torles["command"] = self.torol
        self.kezelogomb.reszlet["command"] = self.mutat

        self.szemely.valaszto.bind("<<ComboboxSelected>>", self.mutat_meglevo_telefon)

        nevsor = [nev["nev"] for nev in kon.select("nev", orderby="nev").fetchall()]
        self.szemely.valaszto["values"] = nevsor
        if nevsor:
            self.szemely.valaszto.current(0)
            self.mutat_meglevo_telefon(None)  # argumentum az event miatt
        else:
            self.szemely.valaszto.set("")

        self.szemely.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.ujtelefon.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)
        self.meglevotelefon.grid(row=2, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=3, column=0, ipadx=2, ipady=2)

    def mutat_meglevo_telefon(self, event):
        rowid = {sor["nev"]: sor["szemely"] for sor in self.kon.select("nev").fetchall()}
        self.azonosito = rowid[self.szemely.valaszto.get()]
        telefonszamok = self.kon.select("telefon", szemely=self.azonosito).fetchall()
        telefonszamok = ["{} ({})".format(szam["telefonszam"], szam["megjegyzes"]) for szam in telefonszamok]
        self.meglevotelefon.valaszto["values"] = telefonszamok
        if telefonszamok:
            self.meglevotelefon.valaszto.current(0)
        else:
            self.meglevotelefon.valaszto.set("")

    def ment(self):
        adatok = self.ujtelefon.export()
        if self.azonosito and adatok["telefonszam"]:
            adatok["szemely"] = self.azonosito
            self.kon.insert("telefon", **adatok)
            self.ujtelefon.beallit()
            self.mutat_meglevo_telefon(None)
            print("Új bejegyzés mentve.")
        else:
            print("Valami elromlott...")

    def torol(self):
        if self.azonosito:
            self.kon.delete("telefon", logic="AND", szemely=self.azonosito, telefonszam=self.meglevotelefon.valaszto.get())
            self.ujtelefon.beallit()
            self.mutat_meglevo_telefon(None)
            print("Bejegyzés törölve.")
        else:
            print("Valami elromlott...")

    def mutat(self):
        szemely = self.kon.select("elerhetoseg", "elerhetoseg", szemely=self.azonosito)
        szemely = szemely.fetchone()
        if szemely:
            print(szemely["elerhetoseg"])


if __name__ == "__main__":
    import tamer
    #szemelyurlap = SzemelyUrlap(kon = tamer.Tamer("szemely.db"), azonosito=1)
    #szemelyurlap.mainloop()
    telefonurlap = TelefonUrlap(tamer.Tamer("szemely.db"))
    telefonurlap.mainloop()
    """nevsor = kon.select("nev").fetchall()
    nevek = {nev["nev"]: nev["szemely"] for nev in nevsor}
    nevsor = [nev["nev"] for nev in nevsor]
    ablak = Tk()
    v = Valaszto("személy", nevsor, ablak)
    ablak.mainloop()
    print(nevek[v.valasztas.get()])"""
