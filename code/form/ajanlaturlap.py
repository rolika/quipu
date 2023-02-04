from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import date, timedelta
from tkinter.ttk import LabelFrame
from form.urlap import Valaszto
from csomok.ajanlatkeres import Ajanlatkeres
from csomok.ajanlat import Ajanlat
from konstans import Esely


class AjanlatUrlap(LabelFrame):
    def __init__(self, szulo, **kw):
        super().__init__(szulo, text="ajánlat", **kw)

        self._ajanlatiar = StringVar()
        self._leadva = StringVar()
        self._ervenyes = StringVar()
        self._megjegyzes = StringVar()
        self._esely = IntVar()

        rovidek = Frame(self)

        ar = LabelFrame(rovidek, text="ajánlati ár")
        self._fokusz = Entry(ar, textvariable=self._ajanlatiar, width=10)
        self._fokusz.pack(ipadx=2, ipady=2, side=LEFT)
        Label(ar, text="Ft").pack(ipadx=2, ipady=2)
        ar.pack(padx=2, ipady=2, side=LEFT)

        leadva = LabelFrame(rovidek, text="leadva")
        Entry(leadva, textvariable=self._leadva, width=10).pack(ipadx=2, ipady=2)
        leadva.pack(ipadx=2, ipady=2, side=LEFT, padx=10)

        ervenyes = LabelFrame(rovidek, text="érvényes")
        Entry(ervenyes, textvariable=self._ervenyes, width=10).pack(ipadx=2, ipady=2)
        ervenyes.pack(ipadx=2, ipady=2, side=LEFT)

        rovidek.pack(ipadx=2, ipady=2, fill=BOTH)

        esely = LabelFrame(self, text="esélylatolgatás")
        Radiobutton(esely, variable=self._esely, text="bukott", value=Esely.BUKOTT.ertek).pack(ipadx=2, ipady=2, side=LEFT)
        Radiobutton(esely, variable=self._esely, text="normál", value=Esely.NORMAL.ertek).pack(ipadx=2, ipady=2, side=LEFT)
        Radiobutton(esely, variable=self._esely, text="érdekes", value=Esely.ERDEKES.ertek).pack(ipadx=2, ipady=2, side=LEFT)
        Radiobutton(esely, variable=self._esely, text="végső", value=Esely.VEGSO.ertek).pack(ipadx=2, ipady=2)
        esely.pack(ipadx=2, ipady=2, fill=BOTH)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes, width=40).pack(ipadx=2, ipady=2, side=LEFT)
        megjegyzes.pack(ipadx=2, ipady=2, fill=BOTH)

    @property
    def fokusz(self):
        return self._fokusz

    def beallit(self, ajanlat):
        self._ajanlatiar.set(ajanlat.ajanlatiar)
        self._leadva.set(ajanlat.leadva)
        self._ervenyes.set(ajanlat.ervenyes)
        if ajanlat.esely not in [esely.value for esely in Esely]:
            ajanlat.esely = Esely.NORMAL.ertek
        self._esely.set(ajanlat.esely)
        self._megjegyzes.set(ajanlat.megjegyzes)

    def export(self):
        return Ajanlat(ajanlatiar=self._ajanlatiar.get(),
                       leadva=self._leadva.get(),
                       ervenyes=self._ervenyes.get(),
                       esely=self._esely.get(),
                       megjegyzes=self._megjegyzes.get())

    def datum_ervenyes(self):
        """Dátumok formátumának és sorrendjének ellenőrzése"""
        try:
            leadva = date.fromisoformat(self._leadva.get())
            ervenyes = date.fromisoformat(self._ervenyes.get())
        except ValueError:
            return False
        if leadva > ervenyes:
            return False
        return True


class UjAjanlatUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon
        super().__init__(szulo, title="Új ajánlat rögzítése")

    def body(self, szulo):
        self._ajanlatkeres_valaszto = Valaszto("ajánlatkérés", self._ajanlatkeresek(), self)
        self._ajanlatkeres_valaszto.set_callback(self._alapertelmezes)
        self._ajanlatkeres_valaszto.pack(ipadx=2, ipady=2, fill=BOTH)

        self._ajanlat_urlap = AjanlatUrlap(self)
        self._ajanlat_urlap.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH)

        self._alapertelmezes(1)
        return self._ajanlatkeres_valaszto.valaszto

    def validate(self):
        if not bool(self._ajanlat_urlap.export()):
            messagebox.showwarning("Hiányos adat!", "Add meg az ajánlati árat!", parent=self)
            return False
        if not self._ajanlat_urlap.datum_ervenyes():
            messagebox.showwarning("Dátumhiba!", "Formátum vagy sorrend hibás!", parent=self)
            return False
        return True

    def apply(self):
        ajanlatkeres = self._ajanlatkeres_valaszto.elem
        ajanlat = self._ajanlat_urlap.export()
        ajanlat.ajanlatkeres = ajanlatkeres.azonosito
        if ajanlat.ment(self._kon.ajanlat):
            print("Árajánlat mentve.")
        else:
            print("Az árajánlatot nem sikerült elmenteni!")

    def _ajanlatkeresek(self):
        # azok az ajánlatkérések kellenek, melyekre még nem született ajánlat
        ajanlatkeresek = self._kon.ajanlat.execute("""
            SELECT *
            FROM ajanlatkeres
            WHERE azonosito NOT IN (
                SELECT ajanlatkeres.azonosito
                FROM ajanlatkeres, ajanlat
                ON ajanlatkeres.azonosito = ajanlat.ajanlatkeres
            );
            """)
        return sorted(map(lambda ajanlatkeres: Ajanlatkeres(kon=self._kon, **ajanlatkeres), ajanlatkeresek), key=repr)

    def _alapertelmezes(self, event):
        ma = date.isoformat(date.today())
        egyhonapmulva = date.isoformat(date.today() + timedelta(days=30))
        self._ajanlat_urlap.beallit(Ajanlat(ajanlatiar="", leadva=ma, ervenyes=egyhonapmulva, megjegyzes=""))


class AjanlatTorloUrlap(simpledialog.Dialog):
    """Csak ajánlatkérést lehet törölni, és csak olyat, amire nem született még ajánlat."""
    def __init__(self, szulo, kon):
        self._kon = kon
        super().__init__(szulo, title="Ajánlat törlése")

    def body(self, szulo):
        self._ajanlat_valaszto = Valaszto("ajánlat", self._ajanlatok(), szulo)
        self._ajanlat_valaszto.pack(ipadx=2, ipady=2)
        return self._ajanlat_valaszto.valaszto

    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)

    def apply(self):
        ajanlat = self._ajanlat_valaszto.elem
        if ajanlat.torol(self._kon.ajanlat):
            print("Bejegyzés törölve.")
        else:
            print("Nem sikerült törölni!")

    def _ajanlatok(self):
        ajanlatok = self._kon.ajanlat.select("ajanlat")
        return sorted(map(lambda ajanlat: Ajanlat(kon=self._kon, **ajanlat), ajanlatok), key=repr)


class AjanlatModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo, kon):
        self._kon = kon
        super().__init__(szulo, title="Ajánlat módosítása")

    def body(self, szulo):

        self._ajanlat_valaszto = Valaszto("ajánlat", self._ajanlatok(), self)
        self._ajanlat_valaszto.set_callback(self._reszletek)
        self._ajanlat_valaszto.pack(ipadx=2, ipady=2)

        self._ajanlat_urlap = AjanlatUrlap(self)
        self._ajanlat_urlap.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH)

        self._reszletek(1)
        return self._ajanlat_valaszto.valaszto

    def validate(self):
        if not bool(self._ajanlat_urlap.export()):
            messagebox.showwarning("Hiányos adat!", "Add meg az ajánlati árat!", parent=self)
            return False
        if not self._ajanlat_urlap.datum_ervenyes():
            messagebox.showwarning("Dátumhiba!", "Formátum vagy sorrend hibás!", parent=self)
            return False
        return True

    def apply(self):
        meglevo_ajanlat = self._ajanlat_valaszto.elem
        modositott_ajanlat = self._ajanlat_urlap.export()
        meglevo_ajanlat.adatok = modositott_ajanlat
        if meglevo_ajanlat.ment(self._kon.ajanlat):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani!")

    def _ajanlatok(self):
        ajanlatok = self._kon.ajanlat.select("ajanlat")
        return sorted(map(lambda ajanlat: Ajanlat(kon=self._kon, **ajanlat), ajanlatok), key=repr)
    
    def _reszletek(self, event):
        """Megjeleníti a kiválasztott ajánlat módosítható részleteit.
        event: tkinter esemény-paraméter (itt nincs rá szükség)"""
        meglevo_ajanlat = self._ajanlat_valaszto.elem
        if not meglevo_ajanlat.leadva:
            meglevo_ajanlat.leadva = date.isoformat(date.today())
        if not meglevo_ajanlat.ervenyes:
            meglevo_ajanlat.ervenyes = date.isoformat(date.today() + timedelta(days=30))
        self._ajanlat_urlap.beallit(meglevo_ajanlat)