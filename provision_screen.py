import tkinter as tk
from api import get_available_flavors, get_available_images, get_available_networks, get_available_security_groups, get_multiple_output_tables

from loading_screen import LoadingScreen
import time

class ProvisionScreen():
    def __init__(self, master, selected_region):
        self.master = master
        self.master.withdraw()
        loading_screen = LoadingScreen(self.master)
        command_list = [
            "microstack.openstack flavor list",
            "microstack.openstack image list",
            "microstack.openstack network list",
            "microstack.openstack security group list"
        ]
        results = get_multiple_output_tables(1, command_list)
        flavors = get_available_flavors(results[0])
        images = get_available_images(results[1])
        networks = get_available_networks(results[2])
        sec_groups = get_available_security_groups(results[3])
        loading_screen.destroy()
        self.master.deiconify()
        self.master.title("Tela de Provisionamento de VM")
        paddings = {'padx': 5, 'pady': 5}
