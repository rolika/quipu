"""A Quipu általános, többször használt űrlapjai."""

from tkinter import *
from tkinter.ttk import Combobox
from telefon import Telefon
from e_mail import Email
from cim import Cim
from konstans import ELERHETOSEG_TIPUS, CIM_TIPUS, ORSZAG, MEGYE
from szemely import Szemely


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
        Entry(self, textvariable=self._iranyitoszam, width=8).grid(row=2, column=1, sticky=W, padx=2, pady=2)

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
        self._megye.set(cim.megye)
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
    """Csomók megjelenítésére szabott Combobox, egy LabelFrame-be ágyazva.
        A csomók listanézetét jeleníti meg választékként."""
    def __init__(self, cimke, valasztek, master=None, **kw):
        """LabelFrane benépesítése.
        cimke:  LabelFrame címkéje, a választó neve
        valasztek:  csomók iterábilisa, listanézetük kell legyen
        master:     szülő-widget
        kw:         LabelFrame jellemzői"""
        super().__init__(master=master, text=cimke, **kw)
        self._valasztek = valasztek
        self._valaszto = Combobox(self, width=42)
        self.beallit(valasztek)
        self._valaszto.grid()

    def beallit(self, valasztek):
        """Frissít ia választékot.
        valasztek:  csomók iterábilisa, listanézetük kell legyen"""
        self._valasztek = valasztek
        self._valaszto["values"] = [elem.listanezet() for elem in valasztek]
        try:
            self._valaszto.current(0)
        except TclError:
            self._valaszto.set("")

    @property
    def valaszto(self):
        """Maga a Combobox."""
        return self._valaszto

    @property
    def elem(self):
        """Az éppen kiválasztott csomó."""
        try:
            return self._valasztek[self._valaszto.current()]
        except IndexError:
            return None

    def set_callback(self, fv_ref):
        """Callback-függvény beállítása kívülről.
        fv_ref: függvény referenciája () nélkül"""
        self._valaszto.bind("<<ComboboxSelected>>", fv_ref)


class SzemelyUrlap(Frame):
    """Űrlap személyi adatokhoz."""
    def __init__(self, kon=None, master=None, **kwargs) -> Frame:
        """Az űrlap egy tkinter.Frame-ben helyezkedik el, mert a Frame-en belül lehet .grid-elni a widget-eket,
        viszont a simpledialog.Dialog-on belül csak .pack-olni lehet.
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat
        master: szülő widget
        kwargs: tkinter.Frame tulajdonságait szabályozó értékek"""
        super().__init__(master=master, **kwargs)
        self._kon = kon

        self._elotag = StringVar()
        self._vezeteknev = StringVar()
        self._keresztnev = StringVar()
        self._nem = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="előtag").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._elotag, width=8).grid(row=0, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._vezeteknev, width=32)
        self._fokusz.grid(row=1, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._keresztnev, width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="nem").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="nő", value="nő", variable=self._nem).grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self._nem).grid(row=3, column=2, sticky=W, padx=2, pady=2)
        self._nem.set("férfi")

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32)\
            .grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)

    @property
    def fokusz(self) -> Entry:
        """Az űrlap alapértelmezett widget-je."""
        return self._fokusz

    def beallit(self, szemely) -> None:
        """Adatokkal tölti fel az űrlapot.
        szemely:    szemely.Szemely csomó"""
        self._elotag.set(szemely.elotag)
        self._vezeteknev.set(szemely.vezeteknev)
        self._keresztnev.set(szemely.keresztnev)
        self._nem.set(szemely.nem)
        self._megjegyzes.set(szemely.megjegyzes)

    def export(self) -> Szemely:
        """Beolvassa az űrlap kitöltött mezőit és Személy csomót ad vissza belőlük."""
        return Szemely(kon=self._kon,
            elotag=self._elotag.get(),
            vezeteknev=self._vezeteknev.get(),
            keresztnev=self._keresztnev.get(),
            nem=self._nem.get(),
            megjegyzes=self._megjegyzes.get()
        )