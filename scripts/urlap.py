from tkinter import *
from tkinter.ttk import *


class Szemely(LabelFrame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, text="személy", **kw)

        self.mezo = {
            "elotag": StringVar(),
            "vezeteknev": StringVar(),
            "keresztnev": StringVar(),
            "nem": StringVar(),
            "megjegyzes": StringVar()
        }

        Label(self, text="előtag").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["elotag"], width=8).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["vezeteknev"], width=32)\
            .grid(row=1, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["keresztnev"], width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        self.mezo["nem"].set("férfi")
        Label(self, text="nem").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="nő", value="nő", variable=self.mezo["nem"])\
            .grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self.mezo["nem"])\
            .grid(row=3, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["megjegyzes"], width=32)\
            .grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)


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
        Button(self, text="mégsem", width=8, command = self.quit).grid(row=0, column=1, padx=2, pady=2)
        self.mentes = Button(self, text="mentés", width=8)

        self.torles.grid(row=0, column=0, padx=2, pady=2)
        self.mentes.grid(row=0, column=2, padx=2, pady=2)


class SzemelyUrlap(Frame):
    def __init__(self, master=None, kon=None, azonosito=None, **kw):
        super().__init__(master=master, **kw)

        self.szemely = Szemely()
        self.telefon = Telefon()
        self.email = Email()
        self.kezelogomb = KezeloGomb()

        self.szemely.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        self.telefon.grid(row=1, column=0, ipadx=2, ipady=2)
        self.email.grid(row=2, column=0, ipadx=2, ipady=2)
        self.kezelogomb.grid(row=3, column=0, ipadx=2, ipady=2)

        self.kon = kon
        self.azonosito = azonosito
        if azonosito:
            self.felulir()

    def felulir(self):
        # személy beírása
        szemely = self.kon.select("szemely", azonosito=self.azonosito)
        szemely = szemely.fetchone()
        if szemely:
            szemely = {mezo: szemely[mezo] for mezo in self.szemely.mezo if szemely[mezo]}
            for adat in szemely:
                if self.szemely.mezo.get(adat, None):
                    self.szemely.mezo[adat].set(szemely[adat])
        # telefon beírása
        telefon = self.kon.select("telefon", szemely=self.azonosito)
        telefon = telefon.fetchone()
        if telefon:
            telefon = {mezo: telefon[mezo] for mezo in self.telefon.mezo if telefon[mezo]}
            for adat in telefon:
                if self.telefon.mezo.get(adat, None):
                    self.telefon.mezo[adat].set(telefon[adat])
        # email beírása
        email = self.kon.select("email", szemely=self.azonosito)
        email = email.fetchone()
        if email:
            email = {mezo: email[mezo] for mezo in self.email.mezo if email[mezo]}
            for adat in email:
                if self.email.mezo.get(adat, None):
                    self.email.mezo[adat].set(email[adat])

    def ment(self):
        self.valasztas = "mentés"
        self.quit()

    def torol(self):
        self.valasztas = "törlés"
        self.quit()


if __name__ == "__main__":
    import tamer
    szemelyurlap = SzemelyUrlap(kon = tamer.Tamer("szemely.db"), azonosito=17)
    """ kon = tamer.Tamer("szemely.db")
    szemely = kon.select("szemely", azonosito=20)
    szemely = szemely.fetchone()
    if szemely:
        szemely = {mezo: szemely[mezo] for mezo in szemelyurlap.mezo if szemely[mezo]}
        szemelyurlap.felulir(**szemely) """
    szemelyurlap.mainloop()
