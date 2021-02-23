from tkinter import *
import szemelyurlap
import szervezeturlap
import projekturlap
import ajanlaturlap


class Fomenu(Frame):
    def __init__(self, master=None, szemely_kon=None, szervezet_kon=None,
                 kontakt_kon=None, projekt_kon=None, ajanlat_kon=None, **kw):
        super().__init__(master=master, **kw)

        # főmenü
        szemelymb = Menubutton(self, text="Személy", width=10)
        szervezetmb = Menubutton(self, text="Szervezet", width=10)
        projektmb = Menubutton(self, text="Projekt", width=10)
        raktarmb = Menubutton(self, text="Raktár", width=10)

        # menük
        szemelymenu = SzemelyMenu(szemelymb, szemely_kon, szervezet_kon, kontakt_kon)
        szervezetmenu = SzervezetMenu(szervezetmb, szervezet_kon, szemely_kon, kontakt_kon)
        projektmenu = ProjektMenu(projektmb, projekt_kon, szemely_kon, szervezet_kon, kontakt_kon, ajanlat_kon)

        szemelymb.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        szervezetmb.grid(row=0, column=1, sticky=W, ipadx=2, ipady=2)
        projektmb.grid(row=0, column=2, sticky=W, ipadx=2, ipady=2)
        raktarmb.grid(row=0, column=3, sticky=W, ipadx=2, ipady=2)

        self.grid()


class SzemelyMenu(Menu):
    def __init__(self, mb, szemely_kon, szervezet_kon, kontakt_kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="személy", menu=SzemelyAlmenu(szemely_kon, mb))
        self.add("cascade", label="telefon", menu=TelefonAlmenu(szemely_kon, mb))
        self.add("cascade", label="email", menu=EmailAlmenu(szemely_kon, mb))
        self.add("cascade", label="cím", menu=CimAlmenu(szemely_kon, mb))
        self.add("cascade", label="kontaktszemély", menu=SzemelyKontaktAlmenu(szemely_kon, mb, szervezet_kon, kontakt_kon))


class SzervezetMenu(Menu):
    def __init__(self, mb, szervezet_kon, szemely_kon, kontakt_kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="szervezet", menu=SzervezetAlmenu(szervezet_kon, mb))
        self.add("cascade", label="telefon", menu=SzervezetTelefonAlmenu(szervezet_kon, mb))
        self.add("cascade", label="email", menu=SzervezetEmailAlmenu(szervezet_kon, mb))
        self.add("cascade", label="cím", menu=SzervezetCimAlmenu(szervezet_kon, mb))
        self.add("cascade", label="kontaktszemély", menu=SzervezetKontaktAlmenu(szervezet_kon, mb, szemely_kon, kontakt_kon))

class ProjektMenu(Menu):
    def __init__(self, mb, projekt_kon, szemely_kon, szervezet_kon, kontakt_kon, ajanlat_kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="projekt", menu=ProjektAlmenu(projekt_kon, mb))
        self.add("cascade", label="ajánlat(kérés)",
                 menu=AjanlatAlmenu(ajanlat_kon, mb, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon))


class Alapmenu(Menu):
    def __init__(self, mb):
        super().__init__(mb, tearoff=0)
        self._mb = mb

        self.add("command", label="új", command=self.uj)
        self.add("command", label="törlés", command=self.torol)
        self.add("command", label="módosítás", command=self.modosit)

    @property
    def mb(self):
        return self._mb

    def uj(self):
        raise NotImplementedError

    def torol(self):
        raise NotImplementedError

    def modosit(self):
        raise NotImplementedError


class SzemelyAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szemely_kon = kon

    def uj(self):
        szemelyurlap.UjSzemelyUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def torol(self):
        szemelyurlap.SzemelyTorloUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def modosit(self):
        szemelyurlap.SzemelyModositoUrlap(self.mb.winfo_toplevel(), self._szemely_kon)


class TelefonAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szemely_kon = kon

    def uj(self):
        szemelyurlap.UjTelefonUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def torol(self):
        szemelyurlap.TelefonTorloUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def modosit(self):
        szemelyurlap.TelefonModositoUrlap(self.mb.winfo_toplevel(), self._szemely_kon)


class EmailAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szemely_kon = kon

    def uj(self):
        szemelyurlap.UjEmailUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def torol(self):
        szemelyurlap.EmailTorloUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def modosit(self):
        szemelyurlap.EmailModositoUrlap(self.mb.winfo_toplevel(), self._szemely_kon)


class CimAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szemely_kon = kon

    def uj(self):
        szemelyurlap.UjCimUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def torol(self):
        szemelyurlap.CimTorloUrlap(self.mb.winfo_toplevel(), self._szemely_kon)

    def modosit(self):
        szemelyurlap.CimModositoUrlap(self.mb.winfo_toplevel(), self._szemely_kon)


class SzervezetAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szervezet_kon = kon

    def uj(self):
        szervezeturlap.UjSzervezetUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def torol(self):
        szervezeturlap.SzervezetTorloUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def modosit(self):
        szervezeturlap.SzervezetModositoUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)


class SzervezetTelefonAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szervezet_kon = kon

    def uj(self):
        szervezeturlap.UjTelefonUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def torol(self):
        szervezeturlap.TelefonTorloUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def modosit(self):
        szervezeturlap.TelefonModositoUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)


class SzervezetEmailAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szervezet_kon = kon

    def uj(self):
        szervezeturlap.UjEmailUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def torol(self):
        szervezeturlap.EmailTorloUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def modosit(self):
        szervezeturlap.EmailModositoUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)


class SzervezetCimAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._szervezet_kon = kon

    def uj(self):
        szervezeturlap.UjCimUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def torol(self):
        szervezeturlap.CimTorloUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)

    def modosit(self):
        szervezeturlap.CimModositoUrlap(self.mb.winfo_toplevel(), self._szervezet_kon)


class SzervezetKontaktAlmenu(Alapmenu):
    def __init__(self, szervezet_kon, mb, szemely_kon, kontakt_kon):
        super().__init__(mb)
        self._szervezet_kon = szervezet_kon
        self._szemely_kon = szemely_kon
        self._kontakt_kon = kontakt_kon

    def uj(self):
        self._szervezet_kon.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.UjKontaktUrlap(self.mb.winfo_toplevel(),
                                      self._szervezet_kon,
                                      self._szemely_kon,
                                      self._kontakt_kon)
        self._szervezet_kon.detach("szemely", "kontakt")

    def torol(self):
        self._szervezet_kon.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.KontaktTorloUrlap(self.mb.winfo_toplevel(),
                                         self._szervezet_kon,
                                         self._szemely_kon,
                                         self._kontakt_kon)
        self._szervezet_kon.detach("szemely", "kontakt")

    def modosit(self):
        self._szervezet_kon.attach(szemely="szemely.db", kontakt="kontakt.db")
        szervezeturlap.KontaktModositoUrlap(self.mb.winfo_toplevel(),
                                            self._szervezet_kon,
                                            self._szemely_kon,
                                            self._kontakt_kon)
        self._szervezet_kon.detach("szemely", "kontakt")


class SzemelyKontaktAlmenu(Alapmenu):
    def __init__(self, szemely_kon, mb, szervezet_kon, kontakt_kon):
        super().__init__(mb)
        self._szemely_kon = szemely_kon
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon

    def uj(self):
        self._szemely_kon.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.UjKontaktUrlap(self.mb.winfo_toplevel(),
                                    self._szemely_kon,
                                    self._szervezet_kon,
                                    self._kontakt_kon)
        self._szemely_kon.detach("szervezet", "kontakt")

    def torol(self):
        self._szemely_kon.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.KontaktTorloUrlap(self.mb.winfo_toplevel(),
                                       self._szemely_kon,
                                       self._szervezet_kon,
                                       self._kontakt_kon)
        self._szemely_kon.detach("szervezet", "kontakt")

    def modosit(self):
        self._szemely_kon.attach(szervezet="szervezet.db", kontakt="kontakt.db")
        szemelyurlap.KontaktModositoUrlap(self.mb.winfo_toplevel(),
                                          self._szemely_kon,
                                          self._szervezet_kon,
                                          self._kontakt_kon)
        self._szemely_kon.detach("szervezet", "kontakt")


class ProjektAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._projekt_kon = kon
        self.add("cascade", label="munkarész", menu=MunkareszAlmenu(self._projekt_kon, mb))

    def uj(self):
        projekturlap.UjProjektUrlap(self.mb.winfo_toplevel(), self._projekt_kon)

    def torol(self):
        projekturlap.ProjektTorloUrlap(self.mb.winfo_toplevel(), self._projekt_kon)

    def modosit(self):
        projekturlap.ProjektModositoUrlap(self.mb.winfo_toplevel(), self._projekt_kon)


class MunkareszAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._projekt_kon = kon

    def uj(self):
        projekturlap.UjMunkareszUrlap(self.mb.winfo_toplevel(), self._projekt_kon)

    def torol(self):
        projekturlap.MunkareszTorloUrlap(self.mb.winfo_toplevel(), self._projekt_kon)

    def modosit(self):
        projekturlap.MunkareszModositoUrlap(self.mb.winfo_toplevel(), self._projekt_kon)
    

class AjanlatAlmenu(Alapmenu):
    def __init__(self, ajanlat_kon, mb, szemely_kon, szervezet_kon, kontakt_kon, projekt_kon):
        super().__init__(mb)
        self._ajanlat_kon = ajanlat_kon
        self._szemely_kon = szemely_kon
        self._szervezet_kon = szervezet_kon
        self._kontakt_kon = kontakt_kon
        self._projekt_kon = projekt_kon

    def uj(self):
        ajanlaturlap.UjAjanlatUrlap(self.mb.winfo_toplevel(),
                                    self._ajanlat_kon, 
                                    self._szemely_kon, 
                                    self._szervezet_kon, 
                                    self._kontakt_kon, 
                                    self._projekt_kon)

    def torol(self):
        ajanlaturlap.AjanlatTorloUrlap(self.mb.winfo_toplevel(),
                                       self._ajanlat_kon, 
                                       self._szemely_kon, 
                                       self._szervezet_kon, 
                                       self._kontakt_kon, 
                                       self._projekt_kon)

    def modosit(self):
        ajanlaturlap.AjanlatModositoUrlap(self.mb.winfo_toplevel(),
                                          self._ajanlat_kon, 
                                          self._szemely_kon, 
                                          self._szervezet_kon, 
                                          self._kontakt_kon, 
                                          self._projekt_kon)


if __name__ == "__main__":
    Fomenu(Tk()).mainloop()
