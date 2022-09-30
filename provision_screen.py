import tkinter as tk

class ProvisionScreen():
    def __init__(self, master, selected_region):
        self.master = master
        self.master.title("Tela de Provisionamento de VM")
        paddings = {'padx': 5, 'pady': 5}