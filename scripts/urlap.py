from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import Combobox
from telefon import Telefon
from email import Email
from cim import Cim
from konstans import ELERHETOSEG_TIPUS, CIM_TIPUS, ORSZAG, MEGYE


class TelefonszamUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._telefonszam = StringVar()
        self._megjegyzes = StringVar()
        self._megjegyzes.set(ELERHETOSEG_TIPUS[0])

        Label(self, text="telefonszám").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._telefonszam, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megjegyzes, *ELERHETOSEG_TIPUS).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, telefon):
        self._telefonszam.set(telefon.telefonszam)
        self._megjegyzes.set(telefon.megjegyzes)

    def export(self):
        return Telefon(telefonszam=self._telefonszam.get(), megjegyzes=self._megjegyzes.get())


class EmailcimUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._emailcim = StringVar()
        self._megjegyzes = StringVar()
        self._megjegyzes.set(ELERHETOSEG_TIPUS[0])

        Label(self, text="email-cím").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._emailcim, width=32).grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="megjegyzés").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megjegyzes, *ELERHETOSEG_TIPUS).grid(row=1, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, email):
        self._emailcim.set(email.emailcim)
        self._megjegyzes.set(email.megjegyzes)

    def export(self):
        return Email(emailcim=self._emailcim.get(), megjegyzes=self._megjegyzes.get())


class CimUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self._orszag = StringVar()
        self._megye = StringVar()
        self._megye.set("")
        self._iranyitoszam = StringVar()
        self._helyseg = StringVar()
        self._utca = StringVar()
        self._hrsz = StringVar()
        self._postafiok = StringVar()
        self._honlap = StringVar()
        self._megjegyzes = StringVar()
        self._orszag.set("Magyarország")
        self._megjegyzes.set(CIM_TIPUS[0])

        Label(self, text="ország").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._orszag, *ORSZAG.keys()).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megye").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Combobox(self, textvariable=self._megye, values=MEGYE).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="irányítószám").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        iranyitoszam = Entry(self, textvariable=self._iranyitoszam, width=8)
        iranyitoszam.grid(row=2, column=1, sticky=W, padx=2, pady=2)
        iranyitoszam.focus_set()

        Label(self, text="helység").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._helyseg, width=32).grid(row=3, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="utca, házszám").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._utca, width=32).grid(row=4, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="helyrajzi szám").grid(row=5, column=0, sticky=W, padx=2, pady=2)        
        Entry(self, textvariable=self._hrsz, width=8).grid(row=5, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="postafiók").grid(row=6, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._postafiok, width=8).grid(row=6, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="honlap").grid(row=7, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._honlap, width=32).grid(row=7, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=8, column=0, sticky=W, padx=2, pady=2)
        OptionMenu(self, self._megjegyzes, *CIM_TIPUS).grid(row=8, column=1, sticky=W, padx=2, pady=2)

    def beallit(self, cim):
        self._orszag.set(self._kodbol_orszag(cim.orszag))
        self._iranyitoszam.set(cim.iranyitoszam)
        self._helyseg.set(cim.helyseg)
        self._utca.set(cim.utca)
        self._hrsz.set(cim.hrsz)
        self._postafiok.set(cim.postafiok)
        self._honlap.set(cim.honlap)
        self._megjegyzes.set(cim.megjegyzes)

    def export(self):
        return Cim(
            orszag=ORSZAG[self._orszag.get()],
            megye=self._megye.get(),
            iranyitoszam=self._iranyitoszam.get(),
            helyseg=self._helyseg.get(),
            utca=self._utca.get(),
            hrsz=self._hrsz.get(),
            postafiok=self._postafiok.get(),
            honlap=self._honlap.get(),
            megjegyzes=self._megjegyzes.get()
        )
    
    def _kodbol_orszag(self, kod):
        for orszagnev, orszagkod in ORSZAG.items():
            if orszagkod == kod:
                return orszagnev  # mindig lesz találat


class Valaszto(LabelFrame):
    def __init__(self, cimke, valasztek, master=None, **kw):
        super().__init__(master=master, text=cimke, **kw)
        self._valasztek = valasztek
        self._valaszto = Combobox(self, width=32)
        self.beallit(valasztek)
        self._valaszto.grid()

    def beallit(self, valasztek):
        self._valasztek = valasztek
        self._valaszto["values"] = [elem.listanezet() for elem in valasztek]
        try:
            self._valaszto.current(0)
        except TclError:
            self._valaszto.set("")

    @property
    def valaszto(self):
        return self._valaszto

    @property
    def elem(self):
        try:
            return self._valasztek[self._valaszto.current()]
        except IndexError:
            return None
