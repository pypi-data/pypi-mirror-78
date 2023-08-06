import tkinter as tk

from take_a_break.configuration import CONFIG


class TBSettings(object):
    load_resources = False;

    def __init__(self, parent):
        self._parent = parent
        self._dialog = tk.Tk()
        self._dialog.title("Settings (<ESC> will close it)")
        self._dialog.bind('<Escape>', self.close)
        # self._dialog.minsize(400, 100)
        self._dialog.focus_force()

        canvas1 = tk.Canvas(self._dialog, width=400, height=180)
        canvas1.pack()

        label1 = tk.Label(self._dialog, text="Unsplash Random URL:")
        canvas1.create_window(72, 30, window=label1)

        self.unsplash_provider = tk.Entry(self._dialog, cnf={"width": 63})
        self.unsplash_provider.insert(0, CONFIG.data["unsplash.com"]["url"])
        canvas1.create_window(202, 50, window=self.unsplash_provider)

        label2 = tk.Label(self._dialog, text="Remind me to take a break in (minutes):")
        canvas1.create_window(115, 80, window=label2)

        self.reminder = tk.Entry(self._dialog, cnf={"width": 20})
        self.reminder.insert(0, CONFIG.data["default"]["remind_me_after_these_minutes"])
        canvas1.create_window(73, 100, window=self.reminder)

        label2 = tk.Label(self._dialog, text="Remind me to take a break in (minutes):")
        canvas1.create_window(115, 80, window=label2)

        self.load_resources = CONFIG.load_resources_from_internet()
        self.cbx_load_resources = tk.Checkbutton(self._dialog, text="Load resources from internet ?",
                                                 command=self.check, variable=1)
        if self.load_resources:
            self.cbx_load_resources.select()
        canvas1.create_window(100, 130, window=self.cbx_load_resources)

        button1 = tk.Button(master=self._dialog, text='Save', command=self._save_settings)
        canvas1.create_window(370, 160, window=button1)

    def check(self):
        self.load_resources = not self.load_resources

    def _save_settings(self):
        CONFIG.data["default"]["load_resources_from_internet"] = str(self.load_resources)
        CONFIG.data["default"]["remind_me_after_these_minutes"] = self.reminder.get()
        CONFIG.data["unsplash.com"]["url"] = self.unsplash_provider.get()
        CONFIG.save()
        self.close()

    def show(self):
        self._parent.wm_attributes("-disabled", True)
        self._parent.toplevel_dialog = self._dialog
        self._parent.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.close)
        self._dialog.mainloop()

    def close(self, event=None):
        self._parent.wm_attributes("-disabled", False)  # IMPORTANT!
        self._parent.toplevel_dialog.destroy()
