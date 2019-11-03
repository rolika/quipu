from tkinter import *
from tkinter.ttk import *


class SzemelyForm(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        Label(self, text="személy").grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        Label(self, text="előtag").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self.elotag = StringVar()
        Entry(self, textvariable=self.elotag, width=8).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        self.vezeteknev = StringVar()
        Entry(self, textvariable=self.vezeteknev, width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        self.keresztnev = StringVar()
        Entry(self, textvariable=self.keresztnev, width=32)\
            .grid(row=3, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="nem").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        self.nem = StringVar()
        Radiobutton(self, text="nő", value="nő", variable=self.nem)\
            .grid(row=4, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self.nem)\
            .grid(row=4, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=5, column=0, sticky=W, padx=2, pady=2)
        self.megjegyzes = StringVar()
        Entry(self, textvariable=self.megjegyzes, width=32)\
            .grid(row=5, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Button(self, text="reset", width=8, command=self.reset).grid(row=6, column=0, padx=2, pady=2)
        Button(self, text="mégsem", width=8, command=self.destroy).grid(row=6, column=1, padx=2, pady=2)
        # callback kívülről lesz meghatározható, ezért kell név hozzá
        self.rendben_button = Button(self, text="rendben", width=8, command=self.quit)
        self.rendben_button.grid(row=6, column=2, padx=2, pady=2)

        self.reset()
        self.grid(ipadx=2, ipady=2)

    def reset(self):
        self.elotag.set("")
        self.vezeteknev.set("")
        self.keresztnev.set("")
        self.nem.set("férfi")
        self.megjegyzes.set("")

    def export(self):
        return self.elotag.get(), self.vezeteknev.get(), self.keresztnev.get(), self.nem.get(), self.megjegyzes.get()


class ElerhetosegForm(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        Label(self, text="elérhetőség").grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        Label(self, text="személy").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Combobox(self, width=32).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="email-cím").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        self.emailcim = StringVar()
        Entry(self, textvariable=self.emailcim, width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="telefonszám").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        self.telefonszam = StringVar()
        Entry(self, textvariable=self.telefonszam, width=32)\
            .grid(row=3, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=1, column=2, sticky=E, padx=2, pady=2)
        self.megjegyzes_email = StringVar()
        Entry(self, textvariable=self.megjegyzes_email, width=32).grid(row=2, column=2, sticky=W, padx=2, pady=2)
        self.megjegyzes_telefon = StringVar()
        Entry(self, textvariable=self.megjegyzes_telefon, width=32).grid(row=3, column=2, sticky=W, padx=2, pady=2)

        Button(self, text="reset", width=8, command=self.reset).grid(row=4, column=0, padx=2, pady=2)
        Button(self, text="mégsem", width=8, command=self.destroy).grid(row=4, column=1, sticky=E, padx=2, pady=2)
        # callback kívülről lesz meghatározható, ezért kell név hozzá
        self.rendben_button = Button(self, text="rendben", width=8, command=self.quit)
        self.rendben_button.grid(row=4, column=2, sticky=W, padx=2, pady=2)

        self.reset()
        self.grid(ipadx=2, ipady=2)

    def reset(self):
        self.emailcim.set("")
        self.telefonszam.set("")
        self.megjegyzes_email.set("")
        self.megjegyzes_telefon.set("")

    def export(self):
        return self.emailcim.get(), self.telefonszam.get(), self.megjegyzes_email.get(), self.megjegyzes_telefon.get()


class CimForm(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        Label(self, text="cím").grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        Label(self, text="személy").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Combobox(self, width=32).grid(row=1, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="ország").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Combobox(self, width=8).grid(row=2, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="irányítószám").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        self.iranyitoszam = StringVar()
        Entry(self, textvariable=self.iranyitoszam, width=8).grid(row=3, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="helység").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        self.helyseg = StringVar()
        Entry(self, textvariable=self.helyseg, width=32).grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="utca").grid(row=5, column=0, sticky=W, padx=2, pady=2)
        self.utca = StringVar()
        Entry(self, textvariable=self.utca, width=32).grid(row=5, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=6, column=0, sticky=W, padx=2, pady=2)
        self.megjegyzes = StringVar()
        Entry(self, textvariable=self.megjegyzes, width=32)\
            .grid(row=6, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Button(self, text="reset", width=8).grid(row=7, column=0, padx=2, pady=2)
        Button(self, text="mégsem", width=8, command=self.destroy).grid(row=7, column=1, sticky=E, padx=2, pady=2)
        # callback kívülről lesz meghatározható, ezért kell név hozzá
        self.rendben_button = Button(self, text="rendben", width=8, command=self.quit)
        self.rendben_button.grid(row=7, column=2, sticky=W, padx=2, pady=2)

        self.grid()


if __name__ == "__main__":
    s = Style()
    s.theme_use("alt")
    s.configure(".", font=("Liberation Mono", 10))
    CimForm().mainloop()
