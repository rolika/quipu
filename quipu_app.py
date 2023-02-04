"""
Very simple company management

MIT License

Copyright (c) 2019 Weisz Roland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tkinter import *
from os import getcwd


from code.csomok.alapcsomo import Csomo
#import menu


class Quipu(Frame):
    """ Fő alkalmazás
    A kipu, más néven csomóírás vagy zsinórírás egy különleges, tízes
    számrendszerbeli információtárolási rendszer, melynek segítségével
    helyettesítették az írást az Inka Birodalomban. A kipu a kecsuák nyelvén
    csomót jelent, használati gyakorlatáról bebizonyították, hogy afféle textil
    abakusz, ahol a csomók jelentést hordoznak. A kipukon rögzített értékeket
    meglepő módon egy kettes számrendszeren alapuló, kövek helyzetével operáló,
    számoló eszközzel, egy ősi számítógéppel dolgozták fel. [Wikipedia nyomán]
    """
    def __init__(self, master=None, **kwargs) -> Frame:
        """A fő alkalmazás egy tkinter.Frame-ben indul. Ha a szülője None, mint
        az alapértelmezés, akkor saját ablakot nyit magának.
        master: szülő widget
        kwargs: tkinter.Frame tulajdonságait szabályozó értékek"""
        super().__init__(master=master, **kwargs)

        # adatbázis konnektorok
        # kon = Konnektor()
        # print(getcwd())

        # # alapadatok beírása
        # if not WEVIK.meglevo(kon.szervezet):  # feltételezem, hogy a céggel együtt a többet se írta még be
        #     MAGANSZEMELY.ment(kon.szervezet)  # SQL PRIMARY KEY 1
        #     wevik_id = WEVIK.ment(kon.szervezet)  # SQL PRIMARY KEY 2
        #     vitya_id = VITYA.ment(kon.szemely)  # SQL PRIMARY KEY 1
        #     roli_id = ROLI.ment(kon.szemely)  # SQL PRIMARY KEY 2
        #     Kontakt(szemely=vitya_id, szervezet=wevik_id).ment(kon.kontakt)  # SQL PRIMARY KEY 1
        #     Kontakt(szemely=roli_id, szervezet=wevik_id).ment(kon.kontakt)  # SQL PRIMARY KEY 2
        # MAGANSZEMELY.azonosito = 1
        # WEVIK.azonosito = 2
        # VITYA.azonosito = 1  # a fenti mentési sorrend miatt kontaktszemély-azonosítóként is használandó
        # ROLI.azonosito = 2  # ez is

        # főmenü megjelenítése
        # menu.Fomenu(self, kon)
        # self.grid()

        csomo = Csomo()

        # és pörgés :-)
        self.mainloop()


if __name__ == "__main__":
    app = Quipu()
