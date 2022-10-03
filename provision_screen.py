from ctypes import alignment
from os import access
from re import M
import tkinter as tk
from tkinter import ANCHOR, ttk
from tkinter.tix import COLUMN
from api import get_available_flavors, get_available_images, get_available_networks, get_available_security_groups, get_instantiated_servers, get_multiple_output_tables

from loading_screen import LoadingScreen
import time
from provision_form_modal import ProvisionFormModal

from util import get_server_access_command
COLUMN_HEADING_DICT = {
    'server_name': 'Nome do Servidor',
    'server_status': 'Status do Servidor',
    'server_image': 'Imagem do Servidor',
    'server_flavor': 'Tipo de Servidor',
    'networks': 'Rede'
}

class ProvisionScreen():
    def __init__(self, master, selected_region):
        self.master = master
        self.selected_region = selected_region
        self.selected_element = 0
        self.master.withdraw()
        loading_screen = LoadingScreen(self.master)
        self.load_information()
        loading_screen.destroy()
        self.master.deiconify()
        self.master.title("Tela de Provisionamento de VM")
        table_frame = tk.LabelFrame(self.master, text="Minhas Máquinas Virtuais")
        table_frame.place(relheight=0.5, width=900)
        table_vm = ttk.Treeview(table_frame)
        vm_columns = ['server_name', 'server_status', 'server_image', 'server_flavor', 'networks']
        table_vm['columns'] = vm_columns
        table_vm["show"] = 'headings'

        for column in vm_columns:
            table_vm.heading(column, text=COLUMN_HEADING_DICT[column])
            table_vm.column(column, width=125 if column == 'networks' else 40)
        table_vm.place(height=600, width=900)
        table_vm.bind("<<TreeviewSelect>>", self.select_element)

        i = 0
#         servs = """"
#         +--------------------------------------+-------------+--------+------------------------------------+--------+----------+
# | ID                                   | Name        | Status | Networks                           | Image  | Flavor   |
# +--------------------------------------+-------------+--------+------------------------------------+--------+----------+
# | 284234a3-5849-46ff-9385-19036dd8c384 | test1       | ACTIVE | test=192.168.222.71, 10.20.20.210  | cirros | m1.tiny  |
# | c7815ab7-0485-4642-82b7-299f19f1bfa1 | name-server | ERROR  |                                    | cirros | m1.small |
# | e66e2d11-549c-45bd-81a8-ef4bb1cdfdf2 | test        | ACTIVE | test=192.168.222.34, 10.20.20.20   | cirros | m1.tiny  |
# | d6e88494-65b1-411e-bb45-24a4f49ceb63 | test        | ACTIVE | test=192.168.222.218, 10.20.20.105 | cirros | m1.tiny  |
# +--------------------------------------+-------------+--------+------------------------------------+--------+----------+"""
#         self.servs = get_instantiated_servers(servs)
        for server in self.servers:
            print(server.name)
            # Purposely removing one server for Demonstration (no Login functionality)
            if i != 2:
                table_vm.insert(parent='',index='end',iid=i,text='', values=(server.name, server.status, server.image, server.flavor, server.networks if server.networks != "" else "ERROR"))
            i+=1

        provision_vm_button = tk.Button(self.master, text="Provisionar nova máquina virtual", command=self.on_provision_vm)
        provision_vm_button.place(relx=0.0, rely=0.5)

    def select_element(self, event):
        tree = event.widget
        self.selected_element = int(tree.selection()[0])
        copy_access_command_btn = tk.Button(self.master, text="Obter Comando de Acesso", command=lambda: self.copy_command_to_clipboard())
        copy_access_command_btn.place(rely=0.5, relx=0.30)
        open_vm_btn = tk.Button(self.master, text="Abrir máquina virtual", command=self.on_open_vm)
        open_vm_btn.place(rely=0.5, relx=0.55)

    def on_provision_vm(self):
        toplevel = tk.Toplevel(self.master)
        toplevel.geometry("450x300")
        app = ProvisionFormModal(toplevel, self.flavors, self.images, self.networks, self.sec_groups, self.selected_region)
    
    def copy_command_to_clipboard(self):
        access_command = get_server_access_command(self.servers[self.selected_element].networks)
        self.master.clipboard_clear()
        self.master.clipboard_append(access_command)
        self.master.update()
        command_copied_text = tk.Label(self.master, text="Comando de acesso copiado. Aperte Ctrl + V para usá-lo")
        command_copied_text.place(rely=0.6, relx=0.3)
    
    def on_open_vm(self):
        print("Opening VM")

    def load_information(self):
        command_list = [
            "microstack.openstack flavor list",
            "microstack.openstack image list",
            "microstack.openstack network list",
            "microstack.openstack security group list",
            "microstack.openstack server list"
        ]
        results = get_multiple_output_tables(self.selected_region, command_list)
        self.flavors = get_available_flavors(results[0])
        self.images = get_available_images(results[1])
        self.networks = get_available_networks(results[2])
        self.sec_groups = get_available_security_groups(results[3])
        self.servers = get_instantiated_servers(results[4])
