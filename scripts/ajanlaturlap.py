from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import date, timedelta
from urlap import Valaszto
from projekt import Projekt
from munkaresz import Munkaresz
from szervezet import Szervezet
from szemely import Szemely
from ajanlatkeres import Ajanlatkeres
from ajanlat import Ajanlat
from kontakt import Kontakt
from konstans import Kulcs


class AjanlatkeresUrlap(LabelFrame):
    def __init__(self, szulo, szervezet_kon, szemely_kon, kontakt_kon, projekt_kon, **kw):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        super().__init__(szulo, text="ajánlatkérés adatai", **kw)

        self._erkezett = StringVar()
        self._hatarido = StringVar()
        self._megjegyzes = StringVar()

        ajanlatkero = LabelFrame(self, text="ajánlatkérő")
        self._szervezet_valaszto = Valaszto("szervezet", self._szervezetek(), ajanlatkero)
        self._szervezet_valaszto.set_callback(self._szemely_megjelenit)
        self._szervezet_valaszto.pack(ipadx=2, ipady=2)
        self._szemely_valaszto = Valaszto("személy", self._kontaktszemelyek(), ajanlatkero)
        self._szemely_valaszto.pack(ipadx=2, ipady=2)
        ajanlatkero.pack(ipadx=2, ipady=2)

        projekt = LabelFrame(self, text="ajánlatkérés tárgya")
        self._projekt_valaszto = Valaszto("projekt", self._projektek(), projekt)
        self._projekt_valaszto.set_callback(self._munkaresz_megjelenit)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)
        self._munkaresz_valaszto = Valaszto("munkarész", self._munkareszek(), projekt)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)
        projekt.pack(ipadx=2, ipady=2)

        erkezett = LabelFrame(self, text="érkezett")
        Entry(erkezett, textvariable=self._erkezett, width=10).pack(ipadx=2, ipady=2, side=LEFT)
        erkezett.pack(ipadx=2, ipady=2, fill=BOTH)

        hatarido = LabelFrame(self, text="leadási határidő")
        Entry(hatarido, textvariable=self._hatarido, width=10).pack(ipadx=2, ipady=2, side=LEFT)
        hatarido.pack(ipadx=2, ipady=2, fill=BOTH)

        temafelelos = Frame(self)
        self._temafelelos_valaszto = Valaszto("témafelelős", self._szemelyek(2), temafelelos)
        self._temafelelos_valaszto.pack(ipadx=2, ipady=2, side=LEFT)
        temafelelos.pack(ipadx=2, ipady=2, fill=BOTH)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes, width=40).pack(ipadx=2, ipady=2, side=LEFT)
        megjegyzes.pack(ipadx=2, ipady=2, fill=BOTH)

    def beallit(self, ajanlatkeres):
        self._erkezett.set(ajanlatkeres.erkezett)
        self._hatarido.set(ajanlatkeres.hatarido)
        self._megjegyzes.set(ajanlatkeres.megjegyzes)

    def export(self):
        return Ajanlatkeres(munkaresz=self._munkaresz_valaszto.elem.azonosito,
                            ajanlatkero=self._szemely_valaszto.elem.azonosito,
                            temafelelos=self._temafelelos_valaszto.elem.azonosito,
                            erkezett=self._erkezett.get(),
                            hatarido=self._hatarido.get(),
                            megjegyzes=self._megjegyzes.get())
    def fokusz(self):
        return self._szervezet_valaszto.valaszto

    def _szervezetek(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._szervezet_kon.select("szervezet")), key=repr)

    def _kontaktszemelyek(self):
        szervezet = self._szervezet_valaszto.elem
        if szervezet.azonosito == Kulcs.MAGANSZEMELY.kulcs:
            return self._szemelyek()
        else:
            return self._szemelyek(szervezet.azonosito)

    def _szemelyek(self, szervezet_azonosito=None):
        if szervezet_azonosito:
            lekerdezes = self._szervezet_kon.execute("""
                    SELECT * FROM szemely WHERE azonosito IN (SELECT szemely FROM kontakt WHERE szervezet = ?);
                """, (szervezet_azonosito, ))
        else:  # magánszemély, azaz bárki lehet
            lekerdezes = self._szemely_kon.select("szemely")
        return sorted(map(lambda szemely: Szemely(**szemely), lekerdezes), key=repr)

    def _szemely_megjelenit(self, event):
        self._szemely_valaszto.beallit(self._kontaktszemelyek())

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._projekt_kon.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _munkareszek(self):
        projekt = self._projekt_valaszto.elem
        return sorted(map(lambda munkaresz: Munkaresz(**munkaresz),
                          self._projekt_kon.select("munkaresz", projekt=projekt.azonosito)), key=repr)

    def _munkaresz_megjelenit(self, event):
        self._munkaresz_valaszto.beallit(self._munkareszek())


class AjanlatUrlap(LabelFrame):
    def __init__(self, szulo, **kw):
        super().__init__(szulo, text="ajánlat adatai", **kw)

        self._ajanlatiar = StringVar()
        self._leadva = StringVar()
        self._ervenyes = StringVar()
        self._esely = StringVar()
        self._megjegyzes = StringVar()

        Label(self, text="ajánlati ár").grid(row=0, column=0, sticky=W, padx=2, pady=2)
        self._fokusz = Entry(self, textvariable=self._ajanlatiar, width=10)
        self._fokusz.grid(row=0, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="Ft (nettó)").grid(row=0, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="leadva").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._leadva, width=10).grid(row=1, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="(éééé-hh-nn)").grid(row=1, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="érvényes").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._ervenyes, width=10).grid(row=2, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="(éééé-hh-nn)").grid(row=2, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="esély").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._esely, width=10).grid(row=3, column=1, sticky=W, padx=2, pady=2)
        Label(self, text="%").grid(row=3, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self._megjegyzes, width=32)\
            .grid(row=4, column=1, columnspan=2, sticky=W, padx=2, pady=2)

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
        self._ajanlatkeres_urlap =\
            AjanlatkeresUrlap(szulo, self._szervezet_kon, self._szemely_kon, self._kontakt_kon, self._projekt_kon)
        ma = date.isoformat(date.today())
        egyhetmulva = date.isoformat(date.today() + timedelta(days=7))
        alapertelmezes = Ajanlatkeres(erkezett=ma, hatarido=egyhetmulva, megjegyzes="")
        self._ajanlatkeres_urlap.beallit(alapertelmezes)
        self._ajanlatkeres_urlap.pack(ipadx=4, ipady=4)

        self._ajanlat_urlap = AjanlatUrlap(szulo)
        egyhonapmulva = date.isoformat(date.today() + timedelta(days=30))
        alapertelmezes = Ajanlat(leadva=ma, ervenyes=egyhonapmulva, esely="5", megjegyzes="")
        self._ajanlat_urlap.beallit(alapertelmezes)
        self._ajanlat_urlap.pack(ipadx=4, ipady=4)

        return self._ajanlatkeres_urlap.fokusz()

    def validate(self):
        ajanlatkeres = self._ajanlatkeres_urlap.export()
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
        ajanlatkeres = self._ajanlatkeres_urlap.export()
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
        self._projekt_valaszto = Valaszto("projekt", self._projektek(), szulo)
        self._projekt_valaszto.set_callback(self._munkaresz_megjelenit)
        self._projekt_valaszto.pack(ipadx=2, ipady=2)

        self._munkaresz_valaszto = Valaszto("munkarész", self._munkareszek(), szulo)
        self._munkaresz_valaszto.set_callback(self._ajanlatkero_megjelenit)
        self._munkaresz_valaszto.pack(ipadx=2, ipady=2)

        self._ajanlatkero_valaszto = Valaszto("ajánlatkérő", self._ajanlatkerok(), szulo)
        self._ajanlatkero_valaszto.pack(ipadx=2, ipady=2)

        return self._projekt_valaszto.valaszto

    def validate(self):
        return messagebox.askokcancel("Biztos vagy benne?", "VÉGLEGESEN törlődik!", parent=self)

    def apply(self):
        pass

    def _projektek(self):
        projektek = self._projekt_kon.execute("""
            SELECT *                                                        -- válaszd ki
            FROM projekt                                                    -- azokat a projekteket,
            WHERE azonosito IN (                                            -- melyek
                SELECT projekt                                              -- szerepelnek
                FROM munkaresz                                              -- azon munkarészekben,
                WHERE azonosito IN (                                        -- melyek
                    SELECT munkaresz                                        -- szerepelnek
                    FROM ajanlatkeres                                       -- azon ajánlatkérésekben,
                    WHERE azonosito NOT IN (                                -- melyek
                        SELECT ajanlatkeres.azonosito                       -- azonosítói nem találhatók
                        FROM ajanlatkeres, ajanlat                          -- az ajánlatok között,
                        ON ajanlatkeres.azonosito = ajanlat.ajanlatkeres    -- azaz nincs leadott ajánlatuk
                    )
                )
            );
            """)
        return sorted(map(lambda projekt: Projekt(**projekt), projektek),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _munkaresz_megjelenit(self, event):
        self._munkaresz_valaszto.beallit(self._munkareszek())

    def _munkareszek(self):
        projekt = self._projekt_valaszto.elem
        return sorted(map(lambda munkaresz: Munkaresz(**munkaresz),
                              self._projekt_kon.select("munkaresz", projekt=projekt.azonosito)), key=repr)

    def _ajanlatkero_megjelenit(self, event):
        self._ajanlatkero_valaszto.beallit(self._ajanlatkerok())

    def _ajanlatkerok(self):
        munkaresz = self._munkaresz_valaszto.elem
        return sorted(map(self._ajanlatkero,
                          self._ajanlat_kon.select("ajanlatkeres", munkaresz=munkaresz.azonosito)),
                      key=repr)

    def _ajanlatkero(self, ajanlatkeres):
        kontakt = self._kontakt_kon.select("kontakt", azonosito=ajanlatkeres["ajanlatkero"]).fetchone()
        kontakt = Kontakt(**kontakt)
        szemely = self._szemely_kon.select("szemely", azonosito=kontakt.szemely).fetchone()
        szervezet = self._szervezet_kon.select("szervezet", azonosito=kontakt.szervezet).fetchone()
        kontakt.nev = Szemely(**szemely)
        kontakt.ceg = Szervezet(**szervezet)
        return kontakt


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