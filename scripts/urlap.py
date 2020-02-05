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
        self.nem.set("férfi")

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
    def __init__(self, cimke, valasztek, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)
        
        self.valaszto = Combobox(self, values=self.valasztek(valasztek), width=32)
        self.valaszto.grid()
    
    def valasztek(self, valasztek):
        self.rowid = [elem[0] for elem in valasztek]
        return [elem[1] for elem in valasztek]


class KezeloGomb(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.megse = Button(self, text="mégse", width=8)
        self.ok = Button(self, text="OK", width=8)
        
        self.megse.grid(row=0, column=0, padx=2, pady=2)
        self.ok.grid(row=0, column=1, padx=2, pady=2)


class UjSzemelyUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)

        self.master = master
        self.kon = kon

        self.szemely = Szemely(self)
        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["command"] = self.ment

        self.szemely.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)

    def kivalaszt(self):
        szemely = self.kon.select("szemely", azonosito=self.azonosito)
        return szemely.fetchone() or {}

    def ment(self):
        uj = self.szemely.export()
        if uj["vezeteknev"] or uj["keresztnev"]:
            if self.kon.select("szemely", logic="AND", **uj).fetchone():
                Figyelmeztetes("Ez a név már szerepel az adatbázisban.\nKülönböztesd meg a megjegyzésben!", Toplevel())
                return
            self.azonosito = self.kon.insert("szemely", **uj)
            if self.azonosito:
                print("Új bejegyzés mentve.")
        else:
                Figyelmeztetes("Legalább az egyik nevet add meg!", Toplevel())


class SzemelyTorloUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon
        
        self.lista = Valaszto("Személy törlése", self.nevsor(), self)

        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["command"] = self.torol

        self.lista.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)
    
    def nevsor(self):
        szemelyek = self.kon.select("nev", "szemely", "nev", orderby="nev").fetchall()
        return [(szemely["szemely"], szemely["nev"]) for szemely in szemelyek]

    def torol(self):
        azonosito = self.lista.rowid[self.lista.valaszto.current()]
        self.kon.delete("telefon", szemely=azonosito)
        self.kon.delete("email", szemely=azonosito)
        self.kon.delete("cim", szemely=azonosito)
        self.kon.delete("kontakt", szemely=azonosito)
        if self.kon.delete("szemely", azonosito=azonosito):
            print("Bejegyzés törölve.")
        self.lista.valaszto["values"] = self.lista.valasztek(self.nevsor())


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


class Figyelmeztetes(Frame):
    def __init__(self, szoveg, master=None, **kw):
        super().__init__(master=master, **kw)

        Message(self, text=szoveg, aspect=200).grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        Button(self, text="OK", width=8, command=master.destroy).grid(row=1, column=0, ipadx=2, ipady=2)
        
        self.grid()

if __name__ == "__main__":
    import tamer
    #szemelyurlap = SzemelyUrlap(kon = tamer.Tamer("szemely.db"), azonosito=1)
    #szemelyurlap.mainloop()
    #telefonurlap = TelefonUrlap(tamer.Tamer("szemely.db"))
    #telefonurlap.mainloop()
    """nevsor = kon.select("nev").fetchall()
    nevek = {nev["nev"]: nev["szemely"] for nev in nevsor}
    nevsor = [nev["nev"] for nev in nevsor]
    ablak = Tk()
    v = Valaszto("személy", nevsor, ablak)
    ablak.mainloop()
    print(nevek[v.valasztas.get()])"""

    Figyelmeztetes("Ez a név már szerepel az adatbázisban.", Tk()).mainloop()

