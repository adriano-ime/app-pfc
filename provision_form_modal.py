import tkinter as tk
from api import provision_default_vm, provision_vm
from loading_screen import LoadingScreen
import tkinter.messagebox

from server import Server


class ProvisionFormModal():
    def __init__(self, master, flavors, images, networks, sec_groups, region):
        self.flavors = [x.name for x in flavors]
        self.images = [x.name for x in images]
        self.networks = networks
        network_options = [x.name for x in networks]
        self.sec_groups = sec_groups
        sec_group_options = [x.name for x in sec_groups]
        self.region = region

        self.master = master
        self.master.title("Formulário para provisionamento")

        self.network = tk.StringVar(self.master)
        self.flavor = tk.StringVar(self.master)
        self.image = tk.StringVar(self.master)
        self.sec_group = tk.StringVar(self.master)
        self.is_default = tk.IntVar(self.master)
        self.network.set(network_options[0])
        self.flavor.set(self.flavors[0])
        self.image.set(self.images[0])
        self.sec_group.set(sec_group_options[0])

        tk.Label(self.master, text="Nome do Servidor").grid(row=0, sticky=tk.W)
        self.server_name = tk.Entry(self.master).grid(row = 0, column = 1)
        tk.Label(self.master, text="Tipo de servidor").grid(row=1, sticky=tk.W)
        tk.OptionMenu(self.master, self.flavor, *self.flavors).grid(row=1, column=1)
        tk.Label(self.master, text="Imagem").grid(row=2, sticky=tk.W)
        tk.OptionMenu(self.master, self.image, *self.images).grid(row=2, column=1)
        tk.Label(self.master, text="Rede").grid(row=3, sticky=tk.W)
        tk.OptionMenu(self.master, self.network, *network_options).grid(row=3, column=1)
        tk.Label(self.master, text="Grupo de Segurança").grid(row=4, sticky=tk.W)
        tk.OptionMenu(self.master, self.sec_group, *sec_group_options).grid(row=4, column=1)
        tk.Checkbutton(self.master, text="Configurações Default", variable=self.is_default).grid(row=5, column=0)
        tk.Button(self.master, text="Cancelar", command=self.master.withdraw).grid(row=6, column=0)
        tk.Button(self.master, text="Criar", command=self.provision_vm).grid(row=6, column=1)

    def provision_vm(self):
        loading_screen = LoadingScreen(self.master)
        if (self.is_default.get() == 1):
            result = provision_default_vm(self.region, self.server_name)
        else:
            network_id = ""
            sec_group_id = ""
            for network in self.networks:
                if self.network == network.name:
                    network_id = network.id
            for sec_group in self.sec_groups:
                if self.sec_group == sec_group.name:
                    sec_group_id = sec_group.id
            result = provision_vm(self.region, self.server_name, self.flavor, self.image, network_id, sec_group_id)
        print(result)
        tkinter.messagebox.showinfo("Informação", "Máquina virtual provisionada com sucesso. Atualize a tabela para refletir as mudanças")
        loading_screen.destroy()
        tk.Label(self.master, text=result).grid(row=7)
        self.master.withdraw()
        print("VM provisioned")