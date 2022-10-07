from re import S
import tkinter as tk
from mgt_action_selection import ManagementActionSelectorScreen

from provision_screen import ProvisionScreen

class AppSelectorScreen():
    def __init__(self, master):
        self.master = master
        self.master.title("Prova de Conceito - Provisionamento Multi-Cloud")
        paddings = {'padx': 5, 'pady': 5}

        self.user_action_dict = {'Usuário': ['Provisionar'],
                     'Administrador': ['Provisionar', 'Gerenciar']}
        self.region_list = ['Região 1', 'Região 2']

        self.user = tk.StringVar(self.master)
        self.action = tk.StringVar(self.master)
        self.region = tk.StringVar(self.master)

        self.user.set('Usuário')
        self.user.trace('w', self.update_options)
        actions = self.user_action_dict[self.user.get()]
        self.action.set(actions[0])
        self.region.set('Região 1')

        # User Option Menu Widget
        user_label = tk.Label(self.master, text="Selecione o tipo de usuário que deseja acessar o sistema:")
        user_label.grid(column=0, row=0, sticky=tk.W, **paddings)
        self.user_option_menu = tk.OptionMenu(self.master, self.user, *self.user_action_dict.keys())
        self.user_option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        # Action Option Menu Widget
        action_label = tk.Label(self.master, text="Selecione a seção que deseja acessar no sistema: ")
        action_label.grid(column=0, row=1, sticky=tk.W, **paddings)
        self.action_option_menu = tk.OptionMenu(self.master, self.action, '')
        self.action_option_menu.grid(column=1, row=1, sticky=tk.W, **paddings)

        # Region Option Menu Widget
        region_label = tk.Label(self.master, text="Selecione a região que deseja trabalhar:")
        region_label.grid(column=0, row=2, sticky=tk.W, **paddings)
        self.region_option_menu = tk.OptionMenu(self.master, self.region, *self.region_list)
        self.region_option_menu.grid(column=1, row=2, sticky=tk.W, **paddings)

        # Continue Button Widget
        self.continue_button = tk.Button(self.master, text="Continuar", command=self.on_continue)
        self.continue_button.grid(column=0, row=3, sticky=tk.W, **paddings)

    def on_continue(self):
        selected_region = 1 if self.region.get() == "Região 1" else 2
        if (self.action.get() == "Provisionar"):
            self.master.withdraw()
            toplevel = tk.Toplevel(self.master)
            toplevel.geometry("900x600")
            app = ProvisionScreen(toplevel, selected_region, "user" if self.user.get() == "Usuário" else "admin_provision")
        else:
            self.master.withdraw()
            toplevel = tk.Toplevel(self.master)
            toplevel.geometry("600x400")
            app = ManagementActionSelectorScreen(toplevel, selected_region)


    def update_options(self, *args):
        actions = self.user_action_dict[self.user.get()]
        self.action.set(actions[0])

        menu = self.action_option_menu['menu']
        menu.delete(0, 'end')

        for action in actions:
            menu.add_command(label=action, command=lambda selected_action=action: self.action.set(selected_action))