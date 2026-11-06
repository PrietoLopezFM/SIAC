import tkinter as tk

from config import constants as cons
from util import util_window
from formulario.login import LoginFormular, RegisterFormular

class ApplicationFormular(tk.Tk):
    # This class calls other windows as the program runs.

    def __init__(self):
        super().__init__()

        self.login_window = None
        self.register_window = None

        self.config_window()
        self.build_widgets()

    def config_window(self):
        # Configuración inicial de la ventana
        self.title("SIAC")

        # Configurar el color de fondo y hacer transparente la ventana
        self.configure(bg=cons.C_DE_FONDO_LIGHT)
        self.attributes("-alpha", 0.96)

        w, h = 370, 570
        util_window.centrar_ventana(self, w, h)

    def build_widgets(self):
        tk.Label(
            self,
            text="SIAC",
            font=("Arial", 24),
            bg=cons.C_DE_FONDO_LIGHT,
        ).pack(pady=30)

        tk.Button(
            self,
            text="Iniciar sesión",
            width=20,
            command=self.open_login,
        ).pack(pady=10)

        tk.Button(
            self,
            text="Crear cuenta",
            width=20,
            command=self.open_register,
        ).pack(pady=10)

    def open_login(self):
        # Open the login window, or bring it to the front if already open.
        if self.login_window is None or not self.login_window.winfo_exists():
            self.login_window = LoginFormular(self)
        else:
            self.login_window.lift()
            self.login_window.focus_force()

    def open_register(self):
        # Open the registration window, or bring it to the front if already open.
        if self.register_window is None or not self.register_window.winfo_exists():
            self.register_window = RegisterFormular(self)
        else:
            self.register_window.lift()
            self.register_window.focus_force()
