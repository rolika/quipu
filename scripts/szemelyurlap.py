from tkinter import *
from tkinter.ttk import *


class SzemelyUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.valasztas = None

        self.mezo = {
            "elotag": StringVar(),
            "vezeteknev": StringVar(),
            "keresztnev": StringVar(),
            "nem": StringVar(),
            "megjegyzes": StringVar()
        }

        Label(self, text="személy").grid(row=0, column=0, columnspan=3, padx=2, pady=2)

        Label(self, text="előtag").grid(row=1, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["elotag"], width=8).grid(row=1, column=1, sticky=W, padx=2, pady=2)

        Label(self, text="vezetéknév").grid(row=2, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["vezeteknev"], width=32)\
            .grid(row=2, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="keresztnév").grid(row=3, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["keresztnev"], width=32)\
            .grid(row=3, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Label(self, text="nem").grid(row=4, column=0, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="nő", value="nő", variable=self.mezo["nem"])\
            .grid(row=4, column=1, sticky=W, padx=2, pady=2)
        Radiobutton(self, text="férfi", value="férfi", variable=self.mezo["nem"])\
            .grid(row=4, column=2, sticky=W, padx=2, pady=2)

        Label(self, text="megjegyzés").grid(row=5, column=0, sticky=W, padx=2, pady=2)
        Entry(self, textvariable=self.mezo["megjegyzes"], width=32)\
            .grid(row=5, column=1, columnspan=2, sticky=W, padx=2, pady=2)

        Button(self, text="törlés", width=8, command=self.torol).grid(row=6, column=0, padx=2, pady=2)
        Button(self, text="mégsem", width=8, command=self.quit).grid(row=6, column=1, padx=2, pady=2)
        Button(self, text="mentés", width=8, command=self.ment).grid(row=6, column=2, padx=2, pady=2)

        self.grid(ipadx=2, ipady=2)
    
    def ment(self):
        self.valasztas = "mentés"
        self.quit()

    def torol(self):
        self.valasztas = "törlés"
        self.quit()
    
    def felulir(self, **adatok):
        for adat in adatok:
            if self.mezo.get(adat, None):
                self.mezo[adat].set(adatok[adat])

    def export(self):
        return {mezo: self.mezo[mezo].get()for mezo in self.mezo}


if __name__ == "__main__":
    s = Style()
    s.theme_use("alt")
    s.configure(".", font=("Liberation Mono", 10))
    form = SzemelyUrlap()
    form.felulir(elotag="mr.", vezeteknev="Weisz", keresztnev="Roland", nem="férfi", megjegyzes="nagyfőnök")
    form.mainloop()
    print(form.export())