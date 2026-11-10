import tkinter as tk

from components.left_menu import LeftMenu
from components.top_bar import TopBar
from components.tarjetas_clubs import PanelPrincipal


class DashboardFormular(tk.Toplevel):
    """
    Info to show:
        'Dashboard'

        FRAME:
            Element: Activity
                Content:
                Name:
                Activity_image.png
                'Info:' + number_current_students
                'Instructor' + Instructor_name
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.build_components()

    """
    Given that we're starting to use COMPONENTS (UI components repeated accross pages)
        We need to assign them a location where to be shown.
        Knowing that the top bar always goes on top and the left menu goes on the left.
            We summon a grid, lock them in place and the rest goes for the rest of the page
    """
    def build_components(self):

        # Layout for the dashboard contents
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top bar spans the width of the dashboard
        top_bar = TopBar(self)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Left menu sits below the top bar
        left_menu = LeftMenu(self)
        left_menu.grid(row=1, column=0, sticky="ns")

        # Main dashboard content
        content = tk.Frame(self)
        content.grid(row=1, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        tk.Label(content, text="Dashboard").grid(
            row=0, column=0, sticky="w", padx=20, pady=20
        )

        tarjetasClubs = PanelPrincipal(self)
        tarjetasClubs.grid(row=1, column=1, sticky="w")

        # to do: Add the activity frame and its content here.
