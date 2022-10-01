import tkinter as tk

class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self,parent)
        self.title("Carregando...")
        tk.Label(self, text="▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▇ ▆ ▅ ▄ ▃ ▁").grid(row=1, column=0, padx=15, pady=15)
        self.update()