from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from urlap import TelefonszamUrlap, EmailcimUrlap, CimUrlap, Valaszto
from szemely import Szemely
from telefon import Telefon
from email import Email
from cim import Cim


class SzervezetUrlap(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        