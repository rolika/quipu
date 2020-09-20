from tkinter import *
import szemelyurlap
import szervezeturlap


class Fomenu(Frame):
    def __init__(self, master=None, szemely_kon=None, szervezet_kon=None, **kw):
        super().__init__(master=master, **kw)

        # főmenü
        szemelymb = Menubutton(self, text="Személy", width=10)
        szervezetmb = Menubutton(self, text="Szervezet", width=10)
        projektmb = Menubutton(self, text="Projekt", width=10)
        raktarmb = Menubutton(self, text="Raktár", width=10)

        # menük
        szemelymenu = SzemelyMenu(szemelymb, szemely_kon, szervezet_kon)
        szervezetmenu = SzervezetMenu(szervezetmb, szervezet_kon, szemely_kon)

        szemelymb.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        szervezetmb.grid(row=0, column=1, sticky=W, ipadx=2, ipady=2)
        projektmb.grid(row=0, column=2, sticky=W, ipadx=2, ipady=2)
        raktarmb.grid(row=0, column=3, sticky=W, ipadx=2, ipady=2)

        self.grid()


class SzemelyMenu(Menu):
    def __init__(self, mb, kon, szervezet_kon=None):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="személy", menu=SzemelyAlmenu(kon, mb))
        self.add("cascade", label="telefon", menu=TelefonAlmenu(kon, mb))
        self.add("cascade", label="email", menu=EmailAlmenu(kon, mb))
        self.add("cascade", label="cím", menu=CimAlmenu(kon, mb))
        self.add("cascade", label="kontaktszemély", menu=SzemelyKontaktAlmenu(kon, mb, szervezet_kon))


class SzervezetMenu(Menu):
    def __init__(self, mb, kon, szemely_kon=None):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="szervezet", menu=SzervezetAlmenu(kon, mb))
        self.add("cascade", label="telefon", menu=SzervezetTelefonAlmenu(kon, mb))
        self.add("cascade", label="email", menu=SzervezetEmailAlmenu(kon, mb))
        self.add("cascade", label="cím", menu=SzervezetCimAlmenu(kon, mb))
        self.add("cascade", label="kontaktszemély", menu=SzervezetKontaktAlmenu(kon, mb, szemely_kon))


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
        self._kon = kon

    def uj(self):
        szemelyurlap.UjSzemelyUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szemelyurlap.SzemelyTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szemelyurlap.SzemelyModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class TelefonAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self.kon = kon

    def uj(self):
        szemelyurlap.UjTelefonUrlap(self.mb.winfo_toplevel(), self.kon)

    def torol(self):
        szemelyurlap.TelefonTorloUrlap(self.mb.winfo_toplevel(), self.kon)

    def modosit(self):
        szemelyurlap.TelefonModositoUrlap(self.mb.winfo_toplevel(), self.kon)


class EmailAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szemelyurlap.UjEmailUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szemelyurlap.EmailTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szemelyurlap.EmailModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class CimAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szemelyurlap.UjCimUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szemelyurlap.CimTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szemelyurlap.CimModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class SzervezetAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon

    def uj(self):
        szervezeturlap.UjSzervezetUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szervezeturlap.SzervezetTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szervezeturlap.SzervezetModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class SzervezetTelefonAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self.kon = kon

    def uj(self):
        szervezeturlap.UjTelefonUrlap(self.mb.winfo_toplevel(), self.kon)

    def torol(self):
        szervezeturlap.TelefonTorloUrlap(self.mb.winfo_toplevel(), self.kon)

    def modosit(self):
        szervezeturlap.TelefonModositoUrlap(self.mb.winfo_toplevel(), self.kon)


class SzervezetEmailAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szervezeturlap.UjEmailUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szervezeturlap.EmailTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szervezeturlap.EmailModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class SzervezetCimAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szervezeturlap.UjCimUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szervezeturlap.CimTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szervezeturlap.CimModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class SzervezetKontaktAlmenu(Alapmenu):
    def __init__(self, kon, mb, szemely_kon):
        super().__init__(mb)
        self._kon = kon
        self._szemely_kon = szemely_kon
    
    def uj(self):
        szervezeturlap.UjKontaktUrlap(self.mb.winfo_toplevel(), self._kon, self._szemely_kon)

    def torol(self):
        szervezeturlap.KontaktTorloUrlap(self.mb.winfo_toplevel(), self._kon, self._szemely_kon)

    def modosit(self):
        szervezeturlap.KontaktModositoUrlap(self.mb.winfo_toplevel(), self._kon, self._szemely_kon)


class SzemelyKontaktAlmenu(Alapmenu):
    def __init__(self, kon, mb, szervezet_kon):
        super().__init__(mb)
        self._kon = kon
        self._szervezet_kon = szervezet_kon
    
    def uj(self):
        szemelyurlap.UjKontaktUrlap(self.mb.winfo_toplevel(), self._kon, self._szervezet_kon)

    def torol(self):
        szemelyurlap.KontaktTorloUrlap(self.mb.winfo_toplevel(), self._kon, self._szervezet_kon)

    def modosit(self):
        szemelyurlap.KontaktModositoUrlap(self.mb.winfo_toplevel(), self._kon, self._szervezet_kon)


if __name__ == "__main__":
    Fomenu(Tk()).mainloop()
