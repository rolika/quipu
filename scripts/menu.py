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
        szemelymenu = SzemelyMenu(szemelymb, szemely_kon)
        szervezetmenu = SzervezetMenu(szervezetmb, szervezet_kon)

        szemelymb.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        szervezetmb.grid(row=0, column=1, sticky=W, ipadx=2, ipady=2)
        projektmb.grid(row=0, column=2, sticky=W, ipadx=2, ipady=2)
        raktarmb.grid(row=0, column=3, sticky=W, ipadx=2, ipady=2)

        self.grid()


class SzemelyMenu(Menu):
    def __init__(self, mb, kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="személy", menu=SzemelyAlmenu(kon, mb))
        self.add("cascade", label="telefon", menu=TelefonAlmenu(kon, mb))
        self.add("cascade", label="email", menu=EmailAlmenu(kon, mb))
        self.add("cascade", label="cím", menu=CimAlmenu(kon, mb))


class SzervezetMenu(Menu):
    def __init__(self, mb, kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="szervezet", menu=SzervezetAlmenu(kon, mb))
        self.add("cascade", label="telefon", menu=SzervezetTelefonAlmenu(kon, mb))
        self.add("cascade", label="email", menu=SzervezetEmailAlmenu(kon, mb))
        self.add("cascade", label="cím", menu=SzervezetCimAlmenu(kon, mb))


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
        szervezeturlap.UjSzervezetTelefonUrlap(self.mb.winfo_toplevel(), self.kon)

    def torol(self):
        szervezeturlap.SzervezetTelefonTorloUrlap(self.mb.winfo_toplevel(), self.kon)

    def modosit(self):
        szervezeturlap.SzervezetTelefonModositoUrlap(self.mb.winfo_toplevel(), self.kon)


class SzervezetEmailAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szervezeturlap.UjSzervezetEmailUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szervezeturlap.SzervezetEmailTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szervezeturlap.SzervezetEmailModositoUrlap(self.mb.winfo_toplevel(), self._kon)


class SzervezetCimAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)
        self._kon = kon
    
    def uj(self):
        szervezeturlap.UjSzervezetCimUrlap(self.mb.winfo_toplevel(), self._kon)

    def torol(self):
        szervezeturlap.SzervezetCimTorloUrlap(self.mb.winfo_toplevel(), self._kon)

    def modosit(self):
        szervezeturlap.SzervezetCimModositoUrlap(self.mb.winfo_toplevel(), self._kon)


if __name__ == "__main__":
    Fomenu(Tk()).mainloop()
