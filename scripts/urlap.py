from tkinter import *
from tkinter.ttk import Combobox


class SzemelyUrlap(LabelFrame):
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


class ElerhetosegUrlap(Frame):
    def __init__(self, cimke, master=None, **kw):
        super().__init__(master=master, **kw)
        self.cimke = cimke
        self.elerhetoseg = StringVar()
        self.megjegyzes = StringVar()
        megjegyzes = ("alapértelmezett", "munkahelyi", "privát")
        self.megjegyzes.set(megjegyzes[0])

        Label(self, text=self.cimke).grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.elerhetoseg, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self.megjegyzes, *megjegyzes).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        self.grid()

    def beallit(self, **adatok):
        self.elerhetoseg.set(adatok.get("telefonszam", adatok.get("emailcim", "")))
        self.megjegyzes.set(adatok.get("megjegyzes"))

    def export(self):
        cimke = "telefonszam" if "telefon" in self.cimke else "emailcim"
        return {cimke: self.elerhetoseg.get(),
                "megjegyzes": self.megjegyzes.get()}


class Valaszto(LabelFrame):
    def __init__(self, cimke, valasztek, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)

        self.valaszto = Combobox(self, width=32)
        self.beallit(valasztek)
        self.valaszto.grid()

    def beallit(self, valasztek):
        self.rowid = [elem[0] for elem in valasztek]
        self.valaszto["values"] = [elem[1] for elem in valasztek]
        try:
            self.valaszto.current(0)
        except TclError:
            self.valaszto.set("")

    def azonosito(self):
        try:
            return self.rowid[self.valaszto.current()]
        except IndexError:
            return None


class KezeloGomb(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.master = master
        self.valasz = False

        self.megse = Button(self, text="mégse", command=self.winfo_toplevel().destroy, width=8)
        self.ok = Button(self, text="OK", command=self.rendben, width=8)

        self.megse.grid(row=0, column=0, padx=2, pady=2)
        self.ok.grid(row=0, column=1, padx=2, pady=2)

    def rendben(self):
        self.valasz = True
        self.winfo_toplevel().destroy()


class UjSzemelyUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon

        self.szemelyurlap = SzemelyUrlap(self)
        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["text"] = "mentés"
        self.kezelogomb.ok["command"] = self.ment

        self.szemelyurlap.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)

        self.grid()

    def ment(self):
        uj = self.szemelyurlap.export()
        if uj["vezeteknev"] or uj["keresztnev"]:
            if self.kon.select("szemely", logic="AND", **uj).fetchone():
                Figyelmeztetes("Ez a név már szerepel az adatbázisban.\nKülönböztesd meg a megjegyzésben!", Toplevel())
                return
            if self.kon.insert("szemely", **uj):
                print("Új bejegyzés mentve.")
        else:
                Figyelmeztetes("Legalább az egyik nevet add meg!", Toplevel())


class SzemelyTorloUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon

        self.lista = Valaszto("Személy törlése", self.nevsor(), self)

        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["text"] = "vissza"
        self.kezelogomb.ok["text"] = "törlés"
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["command"] = self.torol

        self.lista.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=1, column=0, ipadx=2, ipady=2)

        self.grid()

    def nevsor(self):
        szemelyek = self.kon.select("nev", "szemely", "nev", orderby="nev").fetchall()
        return [(szemely["szemely"], szemely["nev"]) for szemely in szemelyek]

    def torol(self):
        azonosito = self.lista.azonosito()
        if azonosito:
            biztos = Figyelmeztetes("Biztos vagy benne?\nMINDEN törlődik!", Toplevel(), csak_ok=False)
            biztos.wait_window(biztos)
            if biztos.gombok.valasz:
                self.kon.delete("telefon", szemely=azonosito)
                self.kon.delete("email", szemely=azonosito)
                self.kon.delete("cim", szemely=azonosito)
                self.kon.delete("kontakt", szemely=azonosito)
                if self.kon.delete("szemely", azonosito=azonosito):
                    print("Bejegyzés törölve.")
                self.lista.beallit(self.nevsor())


class SzemelyModositoUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)

        self.kon = kon

        self.lista = Valaszto("Személy módosítása", self.nevsor(), self)
        self.lista.valaszto.bind("<<ComboboxSelected>>", self.megjelenit)

        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["text"] = "vissza"
        self.kezelogomb.ok["text"] = "módosít"
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["command"] = self.modosit

        self.szemelyurlap = SzemelyUrlap(self)
        self.megjelenit(1)

        self.lista.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.szemelyurlap.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def nevsor(self):
        szemelyek = self.kon.select("nev", "szemely", "nev", orderby="nev").fetchall()
        return [(szemely["szemely"], szemely["nev"]) for szemely in szemelyek]

    def megjelenit(self, event):
        szemely = self.kon.select("szemely", azonosito=self.lista.azonosito()).fetchone()
        self.szemelyurlap.beallit(**szemely)

    def modosit(self):
        azonosito = self.lista.azonosito()
        if azonosito:
            uj = self.szemelyurlap.export()
            if uj["vezeteknev"] or uj["keresztnev"]:
                if self.kon.select("szemely", logic="AND", **uj).fetchone():
                    Figyelmeztetes("Ez a név már szerepel az adatbázisban.\nKülönböztesd meg a megjegyzésben!", Toplevel())
                    return
                if self.kon.update("szemely", self.szemelyurlap.export(), azonosito=azonosito):
                    print("Bejegyzés módosítva.")
                    self.lista.beallit(self.nevsor())
                    self.megjelenit(1)
            else:
                Figyelmeztetes("Legalább az egyik nevet add meg!", Toplevel())


class UjTelefonUrlap(Frame):
    def __init__(self, master=None, kon=None, **kw):
        super().__init__(master=master, **kw)
        self.kon = kon
        self.lista = Valaszto("Telefon hozzáadása", self.nevsor(), self)
        self.telefonurlap = ElerhetosegUrlap("telefon", self)
        self.kezelogomb = KezeloGomb(self)
        self.kezelogomb.megse["command"] = master.destroy
        self.kezelogomb.ok["text"] = "mentés"
        self.kezelogomb.ok["command"] = self.ment

        self.lista.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.telefonurlap.grid(row=1, column=0, sticky=W, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=2, column=0, ipadx=2, ipady=2)

        self.grid()

    def nevsor(self):
        szemelyek = self.kon.select("nev", "szemely", "nev", orderby="nev").fetchall()
        return [(szemely["szemely"], szemely["nev"]) for szemely in szemelyek]

    def ment(self):
        uj = self.telefonurlap.export()
        if uj["telefonszam"]:
            uj["szemely"] = self.lista.azonosito()
            self.kon.insert("telefon", **uj)
            print("Bejegyzés mentve.")
        else:
            Figyelmeztetes("A telefonszám nem maradhat üresen!", Toplevel())    


class Figyelmeztetes(Frame):
    def __init__(self, szoveg, master=None, csak_ok=True, **kw):
        super().__init__(master=master, **kw)

        Message(self, text=szoveg, aspect=200).grid(row=0, column=0, sticky=W, padx=2, pady=2)
        self.gombok = KezeloGomb(self)
        if csak_ok:
            self.gombok.megse.destroy()
        self.gombok.grid(row=1, column=0, padx=2, pady=2)

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

    # Figyelmeztetes("Ez a név már szerepel az adatbázisban.", Tk()).mainloop()

    ElerhetosegUrlap("telefon").mainloop()

