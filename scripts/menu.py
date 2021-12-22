from tkinter import *
import szemelyurlap
import szervezeturlap
import projekturlap
import ajanlatkeresurlap
import ajanlaturlap
import anyagurlap
import raktarurlap


class Fomenu(Frame):
    """A főmenüből történik az alkalmazás kezelése."""
    def __init__(self, master=None, kon=None, **kw) -> Frame:
        """A főmenü saját tkinter.Frame-ben kap helyet.
        master: szülő widget
        kon:    adazbázis konnektorok gyűjtősztálya
        **kw:   tkinter.Frame tulajdonságát szabályozó értékek"""
        super().__init__(master=master, **kw)

        # főmenü
        ## ezek a pontok jelennek meg a főmenü sorában
        szemelymb = Menubutton(self, text="Személy", width=10)
        szervezetmb = Menubutton(self, text="Szervezet", width=10)
        projektmb = Menubutton(self, text="Projekt", width=10)
        raktarmb = Menubutton(self, text="Raktár", width=10)

        # menük
        ## ezek keltik életre a főmenüt
        szemelymenu = SzemelyMenu(szemelymb, kon)
        szervezetmenu = SzervezetMenu(szervezetmb, kon)
        projektmenu = ProjektMenu(projektmb, kon)
        raktarmenu = RaktarMenu(raktarmb, kon)

        szemelymb.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        szervezetmb.grid(row=0, column=1, sticky=W, ipadx=2, ipady=2)
        projektmb.grid(row=0, column=2, sticky=W, ipadx=2, ipady=2)
        raktarmb.grid(row=0, column=3, sticky=W, ipadx=2, ipady=2)

        self.grid()


class SzemelyMenu(Menu):
    """Személymenü létrehozása és megjelenítése. A tkinter.Menu osztályból származtatva."""
    def __init__(self, mb, kon) -> Menu:
        """Személymenü példányosítása.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="személy", menu=SzemelyAlmenu(mb, kon))
        self.add("cascade", label="telefon", menu=SzemelyTelefonAlmenu(mb, kon))
        self.add("cascade", label="email", menu=SzemelyEmailAlmenu(mb, kon))
        self.add("cascade", label="cím", menu=SzemelyCimAlmenu(mb, kon))
        self.add("cascade", label="kontaktszemély", menu=SzemelyKontaktAlmenu(mb, kon))


class SzervezetMenu(Menu):
    """Szervezetmenü létrehozása és megjelenítése. A tkinter.Menu osztályból származtatva."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetmenü példányosítása.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="szervezet", menu=SzervezetAlmenu(mb, kon))
        self.add("cascade", label="telefon", menu=SzervezetTelefonAlmenu(mb, kon))
        self.add("cascade", label="email", menu=SzervezetEmailAlmenu(mb, kon))
        self.add("cascade", label="cím", menu=SzervezetCimAlmenu(mb, kon))
        self.add("cascade", label="kontaktszemély", menu=SzervezetKontaktAlmenu(mb, kon))


class ProjektMenu(Menu):
    """Projektmenü létrehozása és megjelenítése. A tkinter.Menu osztályból származtatva."""
    def __init__(self, mb, kon) -> Menu:
        """Projektmenü példányosítása.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="projekt", menu=ProjektAlmenu(mb, kon))
        self.add("cascade", label="ajánlatkérés", menu=AjanlatkeresAlmenu(mb, kon))
        self.add("cascade", label="ajánlat", menu=AjanlatAlmenu(mb, kon))


class RaktarMenu(Menu):
    """Raktártmenü létrehozása és megjelenítése. A tkinter.Menu osztályból származtatva."""
    def __init__(self, mb, kon) -> Menu:
        """Raktártmenü példányosítása.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="anyag", menu=AnyagAlmenu(mb, kon))
        self.add("cascade", label="termék", menu=TermekAlmenu(mb, kon))
        self.add("cascade", label="szállítólevél", menu=SzallitolevelAlmenu(mb, kon))


class Alapmenu(Menu):
    def __init__(self, mb, kon=None) -> Menu:
        """Minden menüpont alatt elvégezhető parancsok.
        mb: tkinter.Menubutton példánya (amolyan szülő widget)"""
        super().__init__(mb, tearoff=0)
        self._mb = mb
        self._kon = kon

        self.add("command", label="új", command=self.uj)
        self.add("command", label="törlés", command=self.torol)
        self.add("command", label="módosítás", command=self.modosit)

    def uj(self) -> None:
        """Új csomó létrehozása."""
        raise NotImplementedError

    def torol(self) -> None:
        """Meglévő csomó törlése."""
        raise NotImplementedError

    def modosit(self) -> None:
        """Meglévő csomó módosítása."""
        raise NotImplementedError


class SzemelyAlmenu(Alapmenu):
    """Személykezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Személykezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új személy létrehozására."""
        szemelyurlap.UjSzemelyUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő személy törlésére."""
        szemelyurlap.SzemelyTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő személy módosítására."""
        szemelyurlap.SzemelyModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzemelyTelefonAlmenu(Alapmenu):
    """Személyek telefonos elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Személyek telefonkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése személy új telefonos elérhetőségének létrehozására."""
        szemelyurlap.UjTelefonUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése személy meglévő telefonos elérhetőségének törlésére."""
        szemelyurlap.TelefonTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése személy meglévő telefonos elérhetőségének módosítására."""
        szemelyurlap.TelefonModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzemelyEmailAlmenu(Alapmenu):
    """Személyek email elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Személyek emailkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése személy új email elérhetőségének létrehozására."""
        szemelyurlap.UjEmailUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése személy meglévő email elérhetőségének törlésére."""
        szemelyurlap.EmailTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése személy meglévő email elérhetőségének módosítására."""
        szemelyurlap.EmailModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzemelyCimAlmenu(Alapmenu):
    """Személyek cím elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Személyek címkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése személy új cím elérhetőségének létrehozására."""
        szemelyurlap.UjCimUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése személy meglévő cím elérhetőségének törlésére."""
        szemelyurlap.CimTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése személy meglévő cím elérhetőségének módosítására."""
        szemelyurlap.CimModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzervezetAlmenu(Alapmenu):
    """Szervezetkezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetkezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új szervezet létrehozására."""
        szervezeturlap.UjSzervezetUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő szervezet törlésére."""
        szervezeturlap.SzervezetTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő szervezet módosítására."""
        szervezeturlap.SzervezetModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzervezetTelefonAlmenu(Alapmenu):
    """Szervezetek telefonos elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetek telefonkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése szervezet új telefonos elérhetőségének létrehozására."""
        szervezeturlap.UjTelefonUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése szervezet meglévő telefonos elérhetőségének törlésére."""
        szervezeturlap.TelefonTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése szervezet meglévő telefonos elérhetőségének módosítására."""
        szervezeturlap.TelefonModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzervezetEmailAlmenu(Alapmenu):
    """Szervezetek email elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetek emailkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése szervezet új email elérhetőségének létrehozására."""
        szervezeturlap.UjEmailUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése szervezet meglévő email elérhetőségének törlésére."""
        szervezeturlap.EmailTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése szervezet meglévő email elérhetőségének módosítására."""
        szervezeturlap.EmailModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzervezetCimAlmenu(Alapmenu):
    """Szervezetek cím elérhetőségeit kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetek címkezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése szervezet új cím elérhetőségének létrehozására."""
        szervezeturlap.UjCimUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése szervezet meglévő cím elérhetőségének törlésére."""
        szervezeturlap.CimTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése szervezet meglévő cím elérhetőségének módosítására."""
        szervezeturlap.CimModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzervezetKontaktAlmenu(Alapmenu):
    """Szervezet kontaktszemélyeit kezelő almenü."""
    def __init__(self, mb, kon) -> Menu:
        """Szervezetek kontaktszemély-kezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése szervezethez új kontaktszemély hozzárendelésére."""
        self._kon.szervezet.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.UjKontaktUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("szemely", "kontakt")

    def torol(self) -> None:
        """Űrlap megjelenítése szervezet meglévő kontaktszemélyének törlésére."""
        self._kon.szervezet.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.KontaktTorloUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("szemely", "kontakt")

    def modosit(self) -> None:
        """Űrlap megjelenítése szervezethez meglévő kontaktszemélyének módosítására."""
        self._kon.szervezet.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.KontaktModositoUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("szemely", "kontakt")


class SzemelyKontaktAlmenu(Alapmenu):
    """Kontaktszemélyhez rendelt szervezeteket kezelő almenü."""
    def __init__(self, mb, kon) -> Menu:
        """Kontaktszemélyhez rendelt szervezetek kezelő menüpontjainak élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése kontaktszemélyhez új szervezet hozzárendelésére."""
        self._kon.szemely.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.UjKontaktUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szemely.detach("szervezet", "kontakt")

    def torol(self) -> None:
        """Űrlap megjelenítése kontaktszemélyhez rendelt szervezet törlésére."""
        self._kon.szemely.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.KontaktTorloUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szemely.detach("szervezet", "kontakt")

    def modosit(self) -> None:
        """Űrlap megjelenítése kontaktszemélyhez rendelt szervezet módosítására."""
        self._kon.szemely.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.KontaktModositoUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szemely.detach("szervezet", "kontakt")


class ProjektAlmenu(Alapmenu):
    """Projektkezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Projektkezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)
        self.add("cascade", label="munkarész", menu=MunkareszAlmenu(mb, self._kon))

    def uj(self) -> None:
        """Űrlap megjelenítése új projekt létrehozására."""
        projekturlap.UjProjektUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő projekt törlésére."""
        projekturlap.ProjektTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő projekt módosítására."""
        projekturlap.ProjektModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class MunkareszAlmenu(Alapmenu):
    """Munkarész-kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Munkarész-kezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új munkarész létrehozására."""
        projekturlap.UjMunkareszUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő munkarész törlésére."""
        projekturlap.MunkareszTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő munkarész módosítására."""
        projekturlap.MunkareszModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class AjanlatkeresAlmenu(Alapmenu):
    """Ajánlatkérés-kezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Ajánlatkérés-kezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új ajánlatkérés létrehozására."""
        self._kon.szervezet.attach(szemely="szemely.db", kontakt="kontakt.db")
        ajanlatkeresurlap.UjAjanlatkeresUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("szemely", "kontakt")

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő ajánlatkérés törlésére."""
        self._kon.szervezet.attach(szemely="szemely.db", kontakt="kontakt.db")
        self._kon.projekt.attach(ajanlat="ajanlat.db")
        # ha nincs megjeleníthető ajánlatkérés, a hibát itt elkapom
        try:
            ajanlatkeresurlap.AjanlatkeresTorloUrlap(self._mb.winfo_toplevel(), self._kon)
        except AttributeError:
            print("Nincs törölhető árajánlatkérés.")
        self._kon.szervezet.detach("szemely", "kontakt")
        self._kon.projekt.detach("ajanlat")

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő ajánlatkérés módosítására."""
        ajanlatkeresurlap.AjanlatkeresModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class AjanlatAlmenu(Alapmenu):
    """Ajánlatkezelő alapmenü."""
    def __init__(self, mb, kon) -> Menu:
        """Ajánlatkezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő widget)
        kon:    konnektor.Konnektor adatbázis-gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új ajánlat létrehozására."""
        ajanlaturlap.UjAjanlatUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő ajánlat törlésére."""
        ajanlaturlap.AjanlatTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő ajánlat módosítására."""
        ajanlaturlap.AjanlatModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class AnyagAlmenu(Alapmenu):
    """Anyagokat kezelő almenü."""
    def __init__(self, mb, kon) -> Menu:
        """Termékkezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő-widget)
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új anyag létrehozására."""
        self._kon.szervezet.attach(kontakt="kontakt.db")
        anyagurlap.UjAnyagUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("kontakt")

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő anyag törlésére."""
        self._kon.szervezet.attach(kontakt="kontakt.db")
        anyagurlap.AnyagTorloUrlap(self._mb.winfo_toplevel(), self._kon)
        self._kon.szervezet.detach("kontakt")

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő anyag módosítására."""
        anyagurlap.AnyagModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class TermekAlmenu(Alapmenu):
    """Termékeket (árazott anyagokat) kezelő almenü."""
    def __init__(self, mb, kon) -> Menu:
        """Termékkezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő-widget)
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat"""
        super().__init__(mb, kon)

    def uj(self) -> None:
        """Űrlap megjelenítése új termék létrehozására."""
        anyagurlap.UjTermekUrlap(self._mb.winfo_toplevel(), self._kon)

    def torol(self) -> None:
        """Űrlap megjelenítése meglévő termék törlésére."""
        anyagurlap.TermekTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def modosit(self) -> None:
        """Űrlap megjelenítése meglévő termék módosítására."""
        anyagurlap.TermekModositoUrlap(self._mb.winfo_toplevel(), self._kon)


class SzallitolevelAlmenu(Menu):
    """Raktárkészlet kezelése"""
    def __init__(self, mb, kon) -> Menu:
        """Kivétel-kezelő menüpontok élesítése.
        mb:     tkinter.Menubutton példánya (amolyan szülő-widget)
        kon:    konnektor.Konnektor adatbázis gyűjtőkapcsolat"""
        self._mb = mb
        self._kon = kon
        super().__init__(mb, tearoff=0)

        self.add("command", label="kivét", command=self._kivet)
        self.add("command", label="visszvét", command=self._visszvet)
        self.add("command", label="bevét", command=self._bevet)
        self.add("command", label="töröl", command=self._torol)
        self.add("command", label="módosít", command=self._modosit)

    def _kivet(self) -> None:
        """Űrlap megjelenítése új kivételező szállítólevél létrehozására."""
        raktarurlap.UjKivetSzallitolevelUrlap(self._mb.winfo_toplevel(), self._kon)

    def _visszvet(self) -> None:
        """Űrlap megjelenítése új visszavételező szállítólevél létrehozására."""
        raktarurlap.UjVisszvetSzallitolevelUrlap(self._mb.winfo_toplevel(), self._kon)

    def _bevet(self) -> None:
        """Űrlap megjelenítése új bevételező szállítólevél létrehozására."""
        raktarurlap.UjBevetSzallitolevelUrlap(self._mb.winfo_toplevel(), self._kon)

    def _torol(self) -> None:
        """Űrlap megjelenítése meglévő szállítólevél törlésére."""
        raktarurlap.SzallitolevelTorloUrlap(self._mb.winfo_toplevel(), self._kon)

    def _modosit(self) -> None:
        """Űrlap megjelenítése meglévő szállítólevél módosítására."""
        raktarurlap.SzallitolevelModositoUrlap(self._mb.winfo_toplevel(), self._kon)


if __name__ == "__main__":
    Fomenu(Tk()).mainloop()
