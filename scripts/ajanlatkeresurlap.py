from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import date, timedelta
from tkinter.ttk import LabelFrame
from jelleg import Jelleg
from urlap import Valaszto
from kontakt import Kontakt
from ajanlatkeres import Ajanlatkeres


class AjanlatkeresUrlap(Frame):
    def __init__(self, szulo, ajanlat_kon, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo)

        self._erkezett = StringVar()
        self._hatarido = StringVar()
        self._megjegyzes = StringVar()

        self._kontakt_valaszto = Valaszto("ajánlatkérő", self._kontaktszemelyek(), self)
        self._kontakt_valaszto.pack(ipadx=2, ipady=2)
        self._jelleg_valaszto = Valaszto("projekt", self._jellegek(), self)
        self._jelleg_valaszto.pack(ipadx=2, ipady=2)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes, width=40).pack(ipadx=2, ipady=2, side=LEFT)
        megjegyzes.pack(ipadx=2, ipady=2, side=BOTTOM, fill=BOTH)

        self._temafelelos_valaszto = Valaszto("témafelelős", self._kontaktszemelyek(2), self)
        self._temafelelos_valaszto.pack(ipadx=2, ipady=2, side=BOTTOM)

        erkezett = LabelFrame(self, text="érkezett")
        Entry(erkezett, textvariable=self._erkezett, width=10).pack(ipadx=2, ipady=2)
        erkezett.pack(ipadx=2, ipady=2, side=LEFT)
        hatarido = LabelFrame(self, text="leadási határidő")
        Entry(hatarido, textvariable=self._hatarido, width=10).pack(ipadx=2, ipady=2)
        hatarido.pack(ipadx=2, ipady=2, side=LEFT)        
        ma = date.isoformat(date.today())
        egyhetmulva = date.isoformat(date.today() + timedelta(days=7))
        self._erkezett.set(ma)
        self._hatarido.set(egyhetmulva)
    
    @property
    def fokusz(self):
        return self._kontakt_valaszto.valaszto
    
    def export(self):
        return Ajanlatkeres(jelleg=self._jelleg_valaszto.elem.azonosito,
                            ajanlatkero=self._kontakt_valaszto.elem.azonosito,
                            temafelelos=self._temafelelos_valaszto.elem.azonosito,
                            erkezett=self._erkezett.get(),
                            hatarido=self._hatarido.get(),
                            megjegyzes=self._megjegyzes.get())
    
    def beallit(self, ajanlatkeres):
        ajanlatkero = self._kontakt_kon.select("kontakt", azonosito=ajanlatkeres.ajanlatkero).fetchone()
        ajanlatkero = Kontakt(**ajanlatkero)
        ajanlatkero.szemely_kon = self._szemely_kon
        ajanlatkero.szervezet_kon = self._szervezet_kon
        jelleg = self._projekt_kon.select("jelleg", azonosito=ajanlatkeres.jelleg).fetchone()
        jelleg = Jelleg(**jelleg)
        jelleg.projekt_kon = self._projekt_kon
        temafelelos = self._kontakt_kon.select("kontakt", azonosito=ajanlatkeres.temafelelos).fetchone()
        temafelelos = Kontakt(**temafelelos)
        temafelelosok = self._kontaktszemelyek(2)

        self._kontakt_valaszto.beallit((ajanlatkero, ))
        self._jelleg_valaszto.beallit((jelleg, ))
        self._temafelelos_valaszto.beallit(temafelelosok)
        self._temafelelos_valaszto.valaszto.current(temafelelosok.index(temafelelos))
        self._erkezett.set(ajanlatkeres.erkezett)
        self._hatarido.set(ajanlatkeres.hatarido)
        self._megjegyzes.set(ajanlatkeres.megjegyzes)
    
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


class UjAjanlatkeresUrlap(simpledialog.Dialog):
    def __init__(self, szulo, ajanlat_kon, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Új ajánlatkérés rögzítése")

    def body(self, szulo):
        self._ajanlatkeres_urlap = AjanlatkeresUrlap(self,
                                                     self._ajanlat_kon, 
                                                     self._szemely_kon, 
                                                     self._szervezet_kon, 
                                                     self._kontakt_kon, 
                                                     self._projekt_kon)
        self._ajanlatkeres_urlap.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH)
        return self._ajanlatkeres_urlap.fokusz

    def validate(self):
        ajanlatkeres = self._ajanlatkeres_urlap.export()
        if ajanlatkeres.meglevo(self._ajanlat_kon):
            messagebox.showwarning("Létező ajánlatkérés!", "Megjegyzésben különböztesd meg!", parent=self)
            return False
        # dátumformátumok ellenőrzése
        try:
            erkezett = date.fromisoformat(ajanlatkeres.erkezett)
            hatarido = date.fromisoformat(ajanlatkeres.hatarido)
        except ValueError:
            messagebox.showwarning("Dátumhiba!", "Legalább egy dátum formátuma nem jó!", parent=self)
            return False
        # dátumok egymásutániságának ellenőrzése
        if erkezett > hatarido:
            messagebox.showwarning("Dátumhiba!", "A dátumok nem jól követik egymást!", parent=self)
            return False
        return True

    def apply(self):        
        ajanlatkeres = self._ajanlatkeres_urlap.export()
        if ajanlatkeres.ment(self._ajanlat_kon):
            print("Árajánlatkérés mentve.")
        else:
            print("Nem sikerült elmenteni!")


class AjanlatkeresTorloUrlap(simpledialog.Dialog):
    """Csak ajánlatkérést lehet törölni, és csak olyat, amire nem született még ajánlat."""
    def __init__(self, szulo, ajanlat_kon, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
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
            print("Bejegyzés törölve.")
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


class AjanlatkeresModositoUrlap(simpledialog.Dialog):
    """Csak olyan ajánlatkérést lehet módosítani, amire nem született még ajánlat."""
    def __init__(self, szulo, ajanlat_kon, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        self._ajanlat_kon = ajanlat_kon
        super().__init__(szulo, title="Ajánlatkérés módosítása")

    def body(self, szulo):
        ajanlatkeres = Frame(self)
        self._ajanlatkeres_valaszto = Valaszto("ajánlatkérés", self._ajanlatkeresek(), ajanlatkeres)
        self._ajanlatkeres_valaszto.set_callback(self._megjelenit)
        self._ajanlatkeres_valaszto.pack(ipadx=2, ipady=2)
        self._ajanlatkeres_urlap = AjanlatkeresUrlap(ajanlatkeres,
                                                     self._ajanlat_kon, 
                                                     self._szemely_kon, 
                                                     self._szervezet_kon, 
                                                     self._kontakt_kon, 
                                                     self._projekt_kon)
        self._ajanlatkeres_urlap.pack(padx=2, pady=2, ipadx=2, ipady=2, fill=BOTH, side=BOTTOM)
        ajanlatkeres.pack(ipadx=2, ipady=2, fill=BOTH, side=TOP)
        self._megjelenit(1)
        return self._ajanlatkeres_valaszto.valaszto

    def validate(self):
        return True

    def apply(self):
        ajanlatkeres = self._ajanlatkeres_valaszto.elem
        modositas = self._ajanlatkeres_urlap.export()
        ajanlatkeres.adatok = modositas
        if ajanlatkeres.ment(self._ajanlat_kon):
            print("Bejegyzés módosítva.")
        else:
            print("Nem sikerült módosítani!")
    
    def _megjelenit(self, event):
        self._ajanlatkeres_urlap.beallit(self._ajanlatkeres_valaszto.elem)

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
