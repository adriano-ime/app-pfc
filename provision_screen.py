from ctypes import alignment
from os import access
from re import M
import tkinter as tk
from tkinter import ANCHOR, ttk
from tkinter.tix import COLUMN
import tkinter.messagebox
from api import delete_vm, get_available_flavors, get_available_images, get_available_networks, get_available_security_groups, get_instantiated_servers, get_list_table, get_multiple_output_tables

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
    def __init__(self, master, selected_region, flow):
        self.flow = flow
        self.master = master
        self.selected_region = selected_region
        self.selected_element = 0
        self.master.withdraw()
        loading_screen = LoadingScreen(self.master)
        self.load_information()
        loading_screen.destroy()
        self.master.deiconify()
        title = "Tela de Provisionamento de VM" if flow == "user" else "Gerenciamento de Máquinas Virtuais"
        self.master.title(title)
        table_frame_label = "Minhas Máquinas Virtuais" if flow == "user" else "Máquinas Virtuais do Servidor"
        table_frame = tk.LabelFrame(self.master, text=table_frame_label)
        table_frame.place(relheight=0.5, width=900)
        self.table_vm = ttk.Treeview(table_frame)
        vm_columns = ['server_name', 'server_status', 'server_image', 'server_flavor', 'networks']
        self.table_vm['columns'] = vm_columns
        self.table_vm["show"] = 'headings'

        for column in vm_columns:
            self.table_vm.heading(column, text=COLUMN_HEADING_DICT[column])
            self.table_vm.column(column, width=125 if column == 'networks' else 40)
        self.table_vm.place(height=600, width=900)
        self.table_vm.bind("<<TreeviewSelect>>", self.select_element)
        self.mount_table()

        provision_vm_button = tk.Button(self.master, text="Provisionar nova máquina virtual", command=self.on_provision_vm)
        provision_vm_button.place(relx=0.0, rely=0.5)
        if (self.flow == "admin"):
            delete_vm_btn = tk.Button(self.master, text="Deletar Máquina Virtual", command=self.on_delete_vm)
            delete_vm_btn.place(rely=0.5, relx=0.30)
        refresh_table_btn = tk.Button(self.master, text="Atualizar Tabela", command=self.on_refresh_table)
        refresh_table_btn.place(relx=0.0, rely=0.6)

    def select_element(self, event):
        tree = event.widget
        if(tree.selection()[0] and self.flow == "user"):
            self.selected_element = int(tree.selection()[0])
            copy_access_command_btn = tk.Button(self.master, text="Obter Comando de Acesso", command=lambda: self.copy_command_to_clipboard())
            copy_access_command_btn.place(rely=0.5, relx=0.30)
            open_vm_btn = tk.Button(self.master, text="Abrir máquina virtual", command=self.on_open_vm)
            open_vm_btn.place(rely=0.5, relx=0.55)
            delete_vm_btn = tk.Button(self.master, text="Deletar Máquina Virtual", command=self.on_delete_vm)
            delete_vm_btn.place(rely=0.5, relx=0.80)

    def on_provision_vm(self):
        toplevel = tk.Toplevel(self.master)
        toplevel.geometry("450x300")
        app = ProvisionFormModal(toplevel, self.flavors, self.images, self.networks, self.sec_groups, self.selected_region)
    
    def copy_command_to_clipboard(self):
        access_command = get_server_access_command(self.servers[self.selected_element].networks)
        self.master.clipboard_clear()
        self.master.clipboard_append(access_command)
        self.master.update()
        tkinter.messagebox.showinfo("Informação", "Comando copiado. Use Ctrl (Cmd) + V para usá-lo")
    
    def on_open_vm(self):
        print("Opening VM")
    
    def on_delete_vm(self):
        loading_screen = LoadingScreen(self.master)
        delete_vm(self.selected_region ,self.servers[self.selected_element].id)
        loading_screen.destroy()
        tkinter.messagebox.showinfo("Informação", "Máquina deletada com sucesso. Atualize a tabela para refletir as mudanças")
    
    def mount_table(self):
        self.table_vm.delete(*self.table_vm.get_children())
        i = 0
        if (self.flow == "user"):
            for server in self.servers:
                print(server.name)
                # Purposely removing one server for Demonstration (no Login functionality)
                if i != 2:
                    self.table_vm.insert(parent='',index='end',iid=i,text='', values=(server.name, server.status, server.image, server.flavor, server.networks if server.networks != "" else "ERROR"))
                i+=1
        else:
            for server in self.servers:
                print(server.name)
                self.table_vm.insert(parent='',index='end',iid=i,text='', values=(server.name, server.status, server.image, server.flavor, server.networks if server.networks != "" else "ERROR"))
                i+=1            
    
    def on_refresh_table(self):
        loading_screen = LoadingScreen(self.master)
        self.load_servers()
        self.mount_table()
        loading_screen.destroy()

    def load_servers(self):
        server_list = get_list_table(self.selected_region, "microstack.openstack server list")
        self.servers = get_instantiated_servers(server_list)

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
