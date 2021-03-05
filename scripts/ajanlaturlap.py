from tkinter import *
from tkinter import simpledialog
from datetime import date
from urlap import Valaszto
from projekt import Projekt
from munkaresz import Munkaresz
from szervezet import Szervezet
from szemely import Szemely
from ajanlatkeres import Ajanlatkeres
from konstans import CEGAZONOSITO, JOGI_MAGAN


class AjanlatkeresUrlap(LabelFrame):
    def __init__(self, master, szervezet_kon, szemely_kon, kontakt_kon, projekt_kon, **kw):
        self._szemely_kon = szemely_kon  # super() előtt kell legyenek
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon
        super().__init__(master, text="ajánlatkérés adatai", **kw)

        self._erkezett = StringVar()
        self._hatarido = StringVar()
        self._megjegyzes = StringVar()

        ajanlatkero = LabelFrame(self, text="ajánlatkérő")
        self._szervezet_valaszto = Valaszto("szervezet", self._szervezetek(), ajanlatkero)
        self._szervezet_valaszto.set_callback(self._szemely_megjelenit)
        self._szervezet_valaszto.pack(ipadx=2, ipady=2)
        self._szemely_valaszto = Valaszto("személy", self._szemelyek(), ajanlatkero)
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
        self._temafelelos_valaszto = Valaszto("témafelelős", self._kontaktszemelyek(CEGAZONOSITO), temafelelos)
        self._temafelelos_valaszto.pack(ipadx=2, ipady=2, side=LEFT)
        temafelelos.pack(ipadx=2, ipady=2, fill=BOTH)

        megjegyzes = LabelFrame(self, text="megjegyzés")
        Entry(megjegyzes, textvariable=self._megjegyzes, width=40).pack(ipadx=2, ipady=2, side=LEFT)
        megjegyzes.pack(ipadx=2, ipady=2, fill=BOTH)

    def export(self):
        return Ajanlatkeres(munkaresz=self._munkaresz_valaszto.elem.azonosito,
                            ajanlatkero=self._szemely_valaszto.elem.azonosito,
                            temafelelos=self._temafelelos_valaszto.elem.azonosito,
                            erkezett=self._erkezett.get(),
                            hatarido=self._hatarido.get(),
                            megjegyzes=self._megjegyzes.get())

    def _szervezetek(self):
        return sorted(map(lambda szervezet: Szervezet(**szervezet), self._szervezet_kon.select("szervezet")), key=repr)

    def _szemelyek(self):
        szervezet = self._szervezet_valaszto.elem
        if szervezet.rovidnev in JOGI_MAGAN:
            return self._kontaktszemelyek()
        else:
            return self._kontaktszemelyek(szervezet.azonosito)

    def _szemely_megjelenit(self, event):
        self._szemely_valaszto.beallit(self._szemelyek())

    def _projektek(self):
        return sorted(map(lambda projekt: Projekt(**projekt), self._projekt_kon.select("projekt")),
                      key=lambda elem: (elem.gyakorisag, repr(elem)))

    def _munkareszek(self):
        projekt = self._projekt_valaszto.elem
        return sorted(map(lambda munkaresz: Munkaresz(**munkaresz),
                          self._projekt_kon.select("munkaresz", projekt=projekt.azonosito)), key=repr)

    def _munkaresz_megjelenit(self, event):
        self._munkaresz_valaszto.beallit(self._munkareszek())

    def _kontaktszemelyek(self, szervezet_azonosito=None):
        if szervezet_azonosito:
            lekerdezes = self._szervezet_kon.execute("""
                    SELECT * FROM szemely WHERE azonosito IN (SELECT szemely FROM kontakt WHERE szervezet = ?);
                """, (szervezet_azonosito, ))
        else:  # magánszemély, azaz bárki lehet
            lekerdezes = self._szemely_kon.select("szemely")
        return sorted(map(lambda szemely: Szemely(**szemely), lekerdezes), key=repr)


class UjAjanlatUrlap(simpledialog.Dialog):
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
        super().__init__(szulo, title="Új ajánlat rögzítése")

    def body(self, szulo):

        self._ajanlatkeres_urlap = AjanlatkeresUrlap(szulo,
                                                     self._szervezet_kon,
                                                     self._szemely_kon,
                                                     self._kontakt_kon,
                                                     self._projekt_kon)
        self._ajanlatkeres_urlap.pack(ipadx=4, ipady=4)



    def validate(self):
        return True

    def apply(self):
        pass




class AjanlatTorloUrlap(simpledialog.Dialog):
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
        super().__init__(szulo, title="Ajánlat törlése")


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