import tkinter as tk

from AllPages import AllPages

LARGE_FONT = ("Verdana", 12)


class StarterClass(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label='File', menu=filemenu)

        edit_options = tk.Menu(menubar)
        menubar.add_cascade(label='Edit', menu=edit_options)

        tk.Tk.config(self, menu=menubar)

        self.frames = AllPages(container, self).AllFrames
        self.show_frame("VoiceRecognitionPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


app = StarterClass()
app.geometry("1280x720")  # 690x462
app.mask = []
app.mainloop()
