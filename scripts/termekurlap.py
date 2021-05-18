from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox, LabelFrame
from datetime import date
from urlap import Valaszto
from jelleg import Jelleg
from konstans import TERMEK_TIPUS


class TermekUrlap(Frame):
    """Űrlap termékek jellemzőinek bevitelére."""
    def __init__(self, master=None, **kw):
        """Az űrlap egy saját Frame()-ben jelenik meg.
        master: szülő-widget (ha nincs megadva, saját új ablakban nyílik meg -> tesztelésre)
        **kw:   Frame() paraméterek testreszabáshoz"""
        super().__init__(master=master, **kw)

        self._nev = StringVar()
        self._tipus = StringVar()
        self._cikkszam = StringVar()
        self._egyseg = StringVar()
        self._kiszereles_nev = StringVar()
        self._kiszereles = StringVar()
        self._csomagolas_nev = StringVar()
        self._csomagolas = StringVar()
        self._kritikus = StringVar()
        self._szallitasi_ido = StringVar()
        self._megjegyzes = StringVar()

        #self._gyarto_valaszto = Valaszto("gyártó", self._gyartok(), self)
        #self._gyarto_valaszto.grid(row=0, column=0, sticky=W, padx=2, pady=2)

        Label(self, text="név").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._nev, width=32)
        self._fokusz.grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="típus").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._tipus, *TERMEK_TIPUS).grid(row=2, column=1, sticky=W, padx=2, pady=2)
        self._tipus.set(TERMEK_TIPUS[0])

        Label(self, text="cikkszám").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._cikkszam, width=16).grid(row=3, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="egység").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._egyseg, width=8).grid(row=4, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kiszerelés neve").grid(row=5, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kiszereles_nev, width=8).grid(row=5, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kiszerelés").grid(row=6, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kiszereles, width=8).grid(row=6, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="csomagolás neve").grid(row=7, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._csomagolas_nev, width=8).grid(row=7, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="csomagolás").grid(row=8, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._csomagolas, width=8).grid(row=8, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="kritikus szint").grid(row=9, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._kritikus, width=8).grid(row=9, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="szállítási idő").grid(row=10, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._szallitasi_ido, width=8).grid(row=10, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=11, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32).grid(row=11, column=1, sticky=W, padx=2, pady=2)


if __name__ == "__main__":
    app = TermekUrlap()
    app.pack()
    app.mainloop()