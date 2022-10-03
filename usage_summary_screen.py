import tkinter as tk
from api import get_list_table, get_usage_objects
from tkinter import ttk

from loading_screen import LoadingScreen

COLUMN_HEADING_DICT = {
    "project": "Projeto",
    "num_servers": "Número de Servidores Alocados",
    "mbhours_ram": "Uso de RAM MB-hora",
    "cpu_hours": "Horas CPU",
    "gbhours_disk": "Uso de Disco em GB-horas",
}


class UsageSummaryScreen:
    def __init__(self, master, selected_region):
        self.selected_region = selected_region
        self.master = master
        self.master.withdraw()
        loading_screen = LoadingScreen(self.master)
        self.load_info()
        loading_screen.destroy()
        self.master.deiconify()
        self.master.title("Resumo de Uso da Máquina")
        table_frame = tk.LabelFrame(self.master, text="Minhas Máquinas Virtuais")
        table_frame.place(relheight=0.5, width=900)
        self.table_vm = ttk.Treeview(table_frame)
        vm_columns = [
            "project",
            "num_servers",
            "mbhours_ram",
            "cpu_hours",
            "gbhours_disk",
        ]
        self.table_vm["columns"] = vm_columns
        self.table_vm["show"] = "headings"
        for column in vm_columns:
            self.table_vm.heading(column, text=COLUMN_HEADING_DICT[column])
            self.table_vm.column(column, width=100)
        self.table_vm.place(height=600, width=900)
        self.mount_table()
        
        return_button = tk.Button(self.master, text="Retornar", command=self.master.destroy)
        return_button.place(relx=0.0, rely=0.5)

    def mount_table(self):
        self.table_vm.delete(*self.table_vm.get_children())
        i = 0
        for usage_element in self.usage_objects:
            self.table_vm.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=(
                    usage_element.project,
                    usage_element.num_servers,
                    usage_element.mbhours_ram,
                    usage_element.cpu_hours,
                    usage_element.gbhours_disk,
                ),
            )
            i += 1
    
    def on_return(self):
        self.destroy

    def load_info(self):
        command = "microstack.openstack usage list"
        result = get_list_table(self.selected_region, command)
        self.usage_objects = get_usage_objects(result)
