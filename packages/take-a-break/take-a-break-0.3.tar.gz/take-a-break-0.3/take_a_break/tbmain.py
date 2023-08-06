import tkinter as tk
from time import sleep

from take_a_break import get_resources, get_random_joke
from take_a_break.configuration import CONFIG
from take_a_break.tbmenu import TBMenu
from take_a_break.providers.unsplash_api import UnsplashAPI


class TBMain(object):

    def __init__(self):
        self._main = tk.Tk()
        self.is_visible = True
        self._main.bind('<Escape>', self.quit)
        self._main.title("Take a Break!  (<ESC> will close it)")
        self._main.iconbitmap(default=get_resources('icon.ico'))
        TBMenu(self._main)
        self.focus()

    def show(self, image="random.png"):
        if CONFIG.load_resources_from_internet():
            UnsplashAPI(endpoint=CONFIG.data["unsplash.com"]["url"]).get_random_image()

        width = self._main.winfo_screenwidth()
        height = self._main.winfo_screenheight()
        widget = tk.Label(self._main, cnf={"width": width - 20, "height": height - 110})
        widget.random_png = tk.PhotoImage(file=get_resources(image))
        widget['image'] = widget.random_png
        widget.pack()

        if CONFIG.load_resources_from_internet():
            w = tk.Label(self._main, text=get_random_joke())
            w.pack()
        self._main.mainloop()

    def quit(self, event=None):
        self._main.destroy()

    def focus(self):
        self._main.attributes("-alpha", 1)
        self._main.state('zoomed')

    def switch(self, event=None):
        if self.is_visible:
            self.is_visible = False
            self._fade_out()
            self._main.iconify()
        else:
            self.is_visible = True
            self.focus()

    def _fade_out(self):
        alpha = self._main.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self._main.attributes("-alpha", alpha)
            sleep(0.1)
            self._fade_out()

    def _fade_in(self):
        alpha = self._main.attributes("-alpha")
        if alpha <= 1:
            alpha += .1
            self._main.attributes("-alpha", alpha)
            sleep(0.1)
            self._fade_in()
