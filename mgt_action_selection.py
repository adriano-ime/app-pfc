import tkinter as tk
from provision_screen import ProvisionScreen

from usage_summary_screen import UsageSummaryScreen


class ManagementActionSelectorScreen():
    def __init__(self, master, selected_region):
        self.selected_region = selected_region
        self.master = master
        self.master.title("Seleção de Ação de Gerenciamento")
        ACTIONS = [
            "Resumo de Uso",
            "Gerenciamento de Máquinas Virtuais",
            "Uso Total Servidor",
        ]
        paddings = {'padx': 5, 'pady': 5}

        self.selected_action = tk.StringVar(self.master)

        self.label = tk.Label(self.master, text="Selecione a seção a ser gerenciada:")
        self.label.grid(column=0, row=0, sticky=tk.W, **paddings)
        self.action_menu = tk.OptionMenu(self.master, self.selected_action, *ACTIONS)
        self.action_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        self.continue_button = tk.Button(self.master, text="Continuar", command=self.on_continue)
        self.continue_button.grid(column=0, row=3, sticky=tk.W, **paddings)

    def on_continue(self):
        if(self.selected_action.get() == "Resumo de Uso"):
            toplevel = tk.Toplevel(self.master)
            toplevel.geometry("900x600")
            app = UsageSummaryScreen(toplevel, self.selected_region)
        elif(self.selected_action.get() == "Gerenciamento de Máquinas Virtuais"):
            toplevel = tk.Toplevel(self.master)
            toplevel.geometry("900x600")
            app = ProvisionScreen(toplevel, self.selected_region, "admin")
