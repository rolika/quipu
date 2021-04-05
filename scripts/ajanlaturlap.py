from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import date, timedelta
from tkinter.ttk import LabelFrame
from jelleg import Jelleg
from urlap import Valaszto
from projekt import Projekt
from munkaresz import Munkaresz
from szervezet import Szervezet
from szemely import Szemely
from kontakt import Kontakt
from ajanlatkeres import Ajanlatkeres
from ajanlat import Ajanlat
from konstans import WEVIK


class AjanlatUrlap(LabelFrame):
    def __init__(self, szulo, **kw):
        super().__init__(szulo, text="ajánlat", **kw)

        self._ajanlatiar = StringVar()
        self._leadva = StringVar()
        self._ervenyes = StringVar()
        self._esely = IntVar()
        self._megjegyzes = StringVar()

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

        esely = LabelFrame(self, text="esély")
        Scale(esely, variable=self._esely, label="%", orient=HORIZONTAL, from_=0, to=100, tick=10, length=300)\
            .pack(ipadx=2, ipady=2)
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
        self._esely.set(ajanlat.esely)
        self._megjegyzes.set(ajanlat.megjegyzes)

    def export(self):
        return Ajanlat(ajanlatiar=self._ajanlatiar.get(),
                       leadva=self._leadva.get(),
                       ervenyes=self._ervenyes.get(),
                       esely=self._esely.get(),
                       megjegyzes=self._megjegyzes.get())


class UjAjanlatUrlap(simpledialog.Dialog):
    def __init__(self, szulo, ajanlat_kon, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Új ajánlat rögzítése")

    def body(self, szulo):
        self._erkezett = StringVar()
        self._hatarido = StringVar()
        self._megjegyzes = StringVar()

        ajanlatkeres = LabelFrame(self, text="ajánlatkérés")

        self._kontakt_valaszto = Valaszto("ajánlatkérő", self._kontaktszemelyek(), ajanlatkeres)
        self._kontakt_valaszto.pack(ipadx=2, ipady=2)
        self._jelleg_valaszto = Valaszto("projekt", self._jellegek(), ajanlatkeres)
        self._jelleg_valaszto.pack(ipadx=2, ipady=2)

        megjegyzes = LabelFrame(ajanlatkeres, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes, width=40).pack(ipadx=2, ipady=2, side=LEFT)
        megjegyzes.pack(ipadx=2, ipady=2, side=BOTTOM, fill=BOTH)

        self._temafelelos_valaszto = Valaszto("témafelelős", self._kontaktszemelyek(WEVIK.azonosito), ajanlatkeres)
        self._temafelelos_valaszto.pack(ipadx=2, ipady=2, side=BOTTOM)

        erkezett = LabelFrame(ajanlatkeres, text="érkezett")
        Entry(erkezett, textvariable=self._erkezett, width=10).pack(ipadx=2, ipady=2)
        erkezett.pack(ipadx=2, ipady=2, side=LEFT)
        hatarido = LabelFrame(ajanlatkeres, text="leadási határidő")
        Entry(hatarido, textvariable=self._hatarido, width=10).pack(ipadx=2, ipady=2)
        hatarido.pack(ipadx=2, ipady=2, side=LEFT)        
        ma = date.isoformat(date.today())
        egyhetmulva = date.isoformat(date.today() + timedelta(days=7))
        self._erkezett.set(ma)
        self._hatarido.set(egyhetmulva)

        ajanlatkeres.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH)

        self._ajanlat_urlap = AjanlatUrlap(self)
        ma = date.isoformat(date.today())
        egyhonapmulva = date.isoformat(date.today() + timedelta(days=30))
        ures = Ajanlat(ajanlatiar="", leadva=ma, ervenyes=egyhonapmulva, esely=10, megjegyzes="")
        self._ajanlat_urlap.beallit(ures)
        self._ajanlat_urlap.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH)

        return self._kontakt_valaszto.valaszto

    def validate(self):
        ajanlatkeres = self._get_ajanlatkeres()
        if ajanlatkeres.meglevo(self._ajanlat_kon):
            messagebox.showwarning("Létező ajánlatkérés!", "Megjegyzésben különböztesd meg!", parent=self)
            return False
        ajanlat = self._ajanlat_urlap.export()
        # dátumformátumok ellenőrzése
        try:
            erkezett = date.fromisoformat(ajanlatkeres.erkezett)
            hatarido = date.fromisoformat(ajanlatkeres.hatarido)
            leadva = date.fromisoformat(ajanlat.leadva)
            ervenyes = date.fromisoformat(ajanlat.ervenyes)
        except ValueError:
            messagebox.showwarning("Dátumhiba!", "Legalább egy dátum formátuma nem jó!", parent=self)
            return False
        # dátumok egymásutániságának ellenőrzése
        if erkezett > hatarido or leadva < erkezett or leadva > ervenyes:
            messagebox.showwarning("Dátumhiba!", "A dátumok nem jól követik egymást!", parent=self)
            return False
        return True

    def apply(self):
        ajanlatkeres = self._get_ajanlatkeres()
        ajanlatkeres_azonosito = ajanlatkeres.ment(self._ajanlat_kon)
        if ajanlatkeres_azonosito:
            print("Árajánlatkérés mentve.")
            ajanlat = self._ajanlat_urlap.export()
            if ajanlat.ajanlatiar:
                ajanlat.ajanlatkeres = ajanlatkeres_azonosito
                if ajanlat.ment(self._ajanlat_kon):
                    print("Árajánlat mentve.")
                else:
                    print("Az árajánlatot nem sikerült elmenteni!")
            return
        print("Nem sikerült elmenteni!")
    
    def _kontaktszemelyek(self, szervezet_id=None):
        if szervezet_id:
            kontaktok = self._kontakt_kon.select("kontakt", szervezet=szervezet_id)
        else:
            kontaktok = self._kontakt_kon.select("kontakt")
        return sorted(map(self._kontaktszemely, kontaktok), key=repr)
    
    def _kontaktszemely(self, kontakt):
        kontaktszemely = Kontakt(**kontakt)
        kontaktszemely.szemely_kon = self._szemely_kon
        kontaktszemely.szervezet_kon = self._szervezet_kon
        return kontaktszemely
    
    def _jellegek(self):
        jellegek = self._projekt_kon.select("jelleg")
        return sorted(map(self._jelleg, jellegek), key=repr)
    
    def _jelleg(self, jelleg):
        jelleg = Jelleg(**jelleg)
        jelleg.projekt_kon = self._projekt_kon
        return jelleg
    
    def _get_ajanlatkeres(self):
        return Ajanlatkeres(jelleg=self._jelleg_valaszto.elem.azonosito,
                            ajanlatkero=self._kontakt_valaszto.elem.azonosito,
                            temafelelos=self._temafelelos_valaszto.elem.azonosito,
                            erkezett=self._erkezett.get(),
                            hatarido=self._hatarido.get(),
                            megjegyzes=self._megjegyzes.get())


class AjanlatTorloUrlap(simpledialog.Dialog):
    """Csak ajánlatkérést lehet törölni, és csak olyat, amire nem született még ajánlat."""
    def __init__(self, szulo,
                 ajanlat_kon=None,
                 szemely_kon=None,
                 szervezet_kon=None,
                 kontakt_kon=None,
                 projekt_kon=None):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Ajánlatkérés törlése")

    def body(self, szulo):
        self._ajanlatkeres_valaszto = Valaszto("ajánlatkérés", self._ajanlatkeresek(), szulo)
        self._ajanlatkeres_valaszto.pack(ipadx=2, ipady=2)
        return self._ajanlatkeres_valaszto.valaszto

    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)

    def apply(self):
        ajanlatkeres = self._ajanlatkeres_valaszto.elem
        if ajanlatkeres.torol(self._ajanlat_kon):
            print("Bejegyzés törölve")
        else:
            print("Nem sikerült törölni!")

    def _ajanlatkeresek(self):
        # azok az ajánlatkérések kellenek, melyekre még nem született ajánlat
        ajanlatkeresek = self._ajanlat_kon.execute("""
            SELECT *
            FROM ajanlatkeres
            WHERE azonosito NOT IN (
                SELECT ajanlatkeres.azonosito
                FROM ajanlatkeres, ajanlat
                ON ajanlatkeres.azonosito = ajanlat.ajanlatkeres
            );
            """)
        return sorted(map(self._kon_setter, ajanlatkeresek), key=repr)
    
    def _kon_setter(self, ajanlatkeres):
        ajanlatkeres = Ajanlatkeres(**ajanlatkeres)
        ajanlatkeres.kontakt_kon = self._kontakt_kon
        ajanlatkeres.projekt_kon = self._projekt_kon
        ajanlatkeres.szemely_kon = self._szemely_kon
        ajanlatkeres.szervezet_kon = self._szervezet_kon
        return ajanlatkeres


class AjanlatModositoUrlap(simpledialog.Dialog):
    def __init__(self, szulo,
                 ajanlat_kon=None,
                 szemely_kon=None,
                 szervezet_kon=None,
                 kontakt_kon=None,
                 projekt_kon=None):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Ajánlat módosítása")