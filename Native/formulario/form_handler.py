import tkinter as tk

from config import constants as cons
from util import util_window
from formulario.login import LoginFormular, RegisterFormular


class HomeView(tk.Frame):
    """Vista de inicio: título, subtítulo y botones de acceso."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_widgets()

    def build_widgets(self):
        tk.Label(
            self,
            text="SIAC",
            font=("Arial", 24),
            bg="white",
            fg=cons.COLOR_TITLE_TEXT,
        ).pack(pady=(10, 20))

        tk.Label(
            self,
            text="Sistema Integral de Asistencias y Creditos",
            font=("Arial", 14),
            bg="white",
            fg=cons.COLOR_SUBTITLE_TEXT,
            wraplength=400,
            justify="center",
        ).pack(pady=(0, 20))

        tk.Button(
            self,
            text="Iniciar sesión",
            width=20,
            command=lambda: self.controller.show_view("login"),
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        ).pack(pady=10)

        tk.Button(
            self,
            text="Crear cuenta",
            width=20,
            command=lambda: self.controller.show_view("register"),
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        ).pack(pady=10)


class ApplicationFormular(tk.Tk):
    """Ventana principal: controla el cambio entre inicio, login y registro."""

    # Proporción del frame blanco respecto a la ventana.
    CONTENT_REL_WIDTH = 0.5
    CONTENT_REL_HEIGHT = 0.8

    def __init__(self):
        super().__init__()

        self.views = {
            "home": HomeView,
            "login": LoginFormular,
            "register": RegisterFormular,
        }
        self.current_view = None

        self.config_window()
        self.build_widgets()
        self.show_view("home")

    def config_window(self):
        self.title("SIAC")
        self.configure(bg=cons.COLOR_BACKGROUND_PRIMARY_RED)

        # La ventana más grande deja un borde visible del fondo exterior.
        window_width, window_height = 900, 720
        util_window.centrar_ventana(self, window_width, window_height)

    def build_widgets(self):
        # Frame blanco centrado: ~50% del ancho y ~80% del alto de la ventana.
        content = tk.Frame(self, bg="white")
        content.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=self.CONTENT_REL_WIDTH,
            relheight=self.CONTENT_REL_HEIGHT,
        )
        content.pack_propagate(False)

        # Imágenes fijas en la parte superior (se comparten en todas las vistas).
        images_frame = tk.Frame(content, bg="white")
        images_frame.pack(pady=(20, 0))

        self.image1 = tk.PhotoImage(file="resources/placeholder.png")
        self.image2 = tk.PhotoImage(file="resources/placeholder.png")

        tk.Label(images_frame, image=self.image1, bg="white").grid(
            row=0, column=0, padx=5
        )
        tk.Label(images_frame, image=self.image2, bg="white").grid(
            row=0, column=1, padx=5
        )

        # Contenedor donde se intercambian las vistas.
        self.view_container = tk.Frame(content, bg="white")
        self.view_container.pack(fill="both", expand=True, pady=(10, 10))

    def show_view(self, name):
        """Destruye la vista actual y monta la indicada: home, login o register."""
        if self.current_view is not None:
            self.current_view.destroy()

        view_class = self.views[name]
        self.current_view = view_class(self.view_container, self)
        self.current_view.pack(fill="both", expand=True)