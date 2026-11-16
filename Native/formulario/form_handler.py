import queue
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


from config import constants as cons
from util import util_window
from formulario.login import LoginFormular, RegisterFormular
from database.connection import start_connection


"""
CHANGES APPLIED in this commit:
Added a StartView to first check that the app can connect to the database.
An indeterminate progress bar provides feedback while the connection is attempted.
(The progress bar shows activity, not the actual percentage of connection progress.)

The HomeView (the one that connects to login) is shown after the connection has been made.
"""

class StartView(tk.Frame):
    """First screen: images, app name, and Start button."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.connection_result = None
        self.build_widgets()

    def build_widgets(self):
        images_frame = tk.Frame(self, bg="white")
        images_frame.pack(pady=(20, 10))

        # Keep references to the images so Tkinter doesn't garbage-collect them.
        self.image1 = tk.PhotoImage(file="resources/placeholder.png")
        self.image2 = tk.PhotoImage(file="resources/placeholder.png")

        tk.Label(images_frame, image=self.image1, bg="white").grid(
            row=0, column=0, padx=5
        )
        tk.Label(images_frame, image=self.image2, bg="white").grid(
            row=0, column=1, padx=5
        )

        tk.Label(
            self,
            text="SIAC",
            font=("Arial", 24),
            bg="white",
            fg=cons.COLOR_TITLE_TEXT,
        ).pack(pady=(10, 20))

        self.start_button = tk.Button(
            self,
            text="Iniciar",
            width=20,
            command=self.start_app,
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        )
        self.start_button.pack(pady=10)

        self.progress = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            length=200,
            mode="indeterminate",
        )

    def start_app(self):
        """Start the connection attempt without blocking Tkinter's interface."""
        self.start_button.config(state=tk.DISABLED)
        self.progress.pack(pady=10)
        self.progress.start(10)

        self.connection_result = queue.Queue()

        # The database operation runs in the background so the progress bar can animate.
        threading.Thread(
            target=self._connect_to_database,
            daemon=True,
        ).start()

        self.after(100, self._check_connection)

    def _connect_to_database(self):
        """Attempt the database connection in a background thread."""
        try:
            start_connection()
            self.connection_result.put((True, None))
        except Exception as error:
            self.connection_result.put((False, error))

    def _check_connection(self):
        """Check whether the background connection attempt has finished."""
        try:
            connected, error = self.connection_result.get_nowait()
        except queue.Empty:
            self.after(100, self._check_connection)
            return

        self.progress.stop()
        self.progress.pack_forget()
        self.start_button.config(state=tk.NORMAL)

        if connected:
            self.controller.show_view("home")
        else:
            messagebox.showwarning(
                "No se encuentra la base de datos",
                "No se logró conectar con la base de datos. "
                "Por favor, intenta de nuevo. Si el problema persiste, "
                "contacta a los administradores.",
                parent=self,
            )


class HomeView(tk.Frame):
    """Screen with sign-in and registration options."""

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
            text="Sistema Integral de Asistencias y Créditos",
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
    """Main window and controller for switching between screens."""

    CONTENT_REL_WIDTH = 0.5
    CONTENT_REL_HEIGHT = 0.8

    def __init__(self):
        super().__init__()

        self.views = {
            "start": StartView,
            "home": HomeView,
            "login": LoginFormular,
            "register": RegisterFormular,
        }
        self.current_view = None

        self.config_window()
        self.build_widgets()
        self.show_view("start")

    def config_window(self):
        self.title("SIAC")
        self.configure(bg=cons.COLOR_BACKGROUND_PRIMARY_RED)

        window_width, window_height = 900, 720
        util_window.centrar_ventana(self, window_width, window_height)

    def build_widgets(self):
        content = tk.Frame(self, bg="white")
        content.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=self.CONTENT_REL_WIDTH,
            relheight=self.CONTENT_REL_HEIGHT,
        )

        self.view_container = tk.Frame(content, bg="white")
        self.view_container.pack(fill="both", expand=True, padx=10, pady=10)

    def show_view(self, name):
        """Replace the current view with the requested one."""
        if self.current_view is not None:
            self.current_view.destroy()

        view_class = self.views[name]
        self.current_view = view_class(self.view_container, self)
        self.current_view.pack(fill="both", expand=True)
