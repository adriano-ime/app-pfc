from doctest import master
import tkinter as tk
from api import get_instantiated_servers, get_list_table
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from loading_screen import LoadingScreen

MAX_SERVERS = 10


class TotalServerUsageScreen:
    def __init__(self, master, selected_region):
        self.selected_region = (selected_region,)
        self.master = master
        self.master.withdraw()
        loading_screen = LoadingScreen(self.master)
        self.load_info()
        loading_screen.destroy()
        self.master.deiconify()
        self.master.title("Resumo de Uso da Máquina")
        pie_chart_frame = tk.Frame(self.master)
        pie_chart_frame.pack()

        figure_labels = [
            "Usados (" + str(len(self.servers)) + ")",
            "Não Usados (" + str(MAX_SERVERS - len(self.servers)) + ")",
        ]
        figure_values = [len(self.servers), MAX_SERVERS - len(self.servers)]

        fig = Figure()  # create a figure object
        ax = fig.add_subplot(111)  # add an Axes to the figure

        ax.pie(
            figure_values,
            radius=1,
            labels=figure_labels,
            autopct="%0.2f%%",
            shadow=True,
        )

        chart1 = FigureCanvasTkAgg(fig, pie_chart_frame)
        chart1.get_tk_widget().pack()

    def load_info(self):
        command = "microstack.openstack server list"
        result = get_list_table(self.selected_region[0], command)
        self.servers = get_instantiated_servers(result)
