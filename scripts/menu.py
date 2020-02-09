from tkinter import *
import urlap


class Fomenu(Frame):
    def __init__(self, master=None, szemely_kon=None, **kw):
        super().__init__(master=master, **kw)
        
        # főmenü
        szemelymb = Menubutton(self, text="Személy")
        szervezetmb = Menubutton(self, text="Szervezet")
        projektmb = Menubutton(self, text="Projekt")
        raktarmb = Menubutton(self, text="Raktár")

        # menük
        szemelymenu = Szemelymenu(szemelymb, szemely_kon)

        szemelymb.grid(row=0, column=0, sticky=W, ipadx=2, ipady=2)
        szervezetmb.grid(row=0, column=1, sticky=W, ipadx=2, ipady=2)
        projektmb.grid(row=0, column=2, sticky=W, ipadx=2, ipady=2)
        raktarmb.grid(row=0, column=3, sticky=W, ipadx=2, ipady=2)

        self.grid()


class Szemelymenu(Menu):
    def __init__(self, mb, kon):
        super().__init__(mb, tearoff=0)
        mb["menu"] = self
        self.add("cascade", label="személy", menu=SzemelyAlmenu(kon, mb))


class Alapmenu(Menu):
    def __init__(self, mb):
        super().__init__(mb, tearoff=0)

        self.add("command", label="új", command=self.uj)
        self.add("command", label="töröl", command=self.torol)
        self.add("command", label="módosit", command=self.modosit)
    
    def uj(self):
        raise NotImplementedError

    def torol(self):
        raise NotImplementedError

    def modosit(self):
        raise NotImplementedError


class SzemelyAlmenu(Alapmenu):
    def __init__(self, kon, mb):
        super().__init__(mb)

        self.kon = kon
    
    def uj(self):
        urlap.UjSzemelyUrlap(Toplevel(), self.kon)
    
    def torol(self):
        urlap.SzemelyTorloUrlap(Toplevel(), self.kon)
    
    def modosit(self):
        urlap.SzemelyModositoUrlap(Toplevel(), self.kon)


class TelefonAlmenu(Alapmenu):
    def __init__(self, kon, szulo):
        super().__init__(szulo)

        self.kon = kon

    def uj(self):
        pass

    def torol(self):
        pass

    def modosit(self):
        pass


if __name__ == "__main__":
    Fomenu(Tk()).mainloop()
