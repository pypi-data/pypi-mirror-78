from tkinter import Menu
from tkinter.messagebox import showinfo

from take_a_break.tbsettings import TBSettings


class TBMenu(object):
    def __init__(self, take_a_break):
        self._parent = take_a_break
        self._menu = Menu(self._parent)
        self._file_menu = Menu(self._menu, tearoff=0)
        self._file_menu.add_command(label="Settings", command=self._open_settings)
        self._menu.add_cascade(label="File", menu=self._file_menu)

        self._help_menu = Menu(self._menu, tearoff=0)
        self._help_menu.add_command(label="About", command=self._show_about)
        self._menu.add_cascade(label="Help", menu=self._help_menu)

        take_a_break.config(menu=self._menu)

    def _open_settings(self):
        TBSettings(self._parent).show()

    def _show_about(self):
        showinfo("Take a Break", "created by: Paul Brodner")
