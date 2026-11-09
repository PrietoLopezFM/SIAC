import tkinter as tk
from tkinter import messagebox

from config import constants as cons
from dashboard import DashboardFormular

from models import authenticate_mock, get_person_by_user

# Fondo de las vistas: el mismo del frame blanco de form_handler.
BG = "white"


class AccountsFormular(tk.Frame):
    """Base de las vistas de login y registro (viven dentro de form_handler)."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.show_password = tk.BooleanVar(master=self, value=False)
        self.build_widgets()

    def create_entry(self, **kwargs):
        """Crea un Entry con el estilo del formulario (ej. show="*" para contraseña)."""
        return tk.Entry(
            self,
            width=30,
            bg=cons.COLOR_BACKGROUND_ELEMENTS,
            fg=cons.COLOR_INPUT_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=cons.COLOR_BORDER_ELEMENTS,  # borde sin foco
            highlightcolor=cons.COLOR_BORDER_ELEMENTS,       # borde con foco
            **kwargs,
        )

    def build_widgets(self):
        """Crea los campos compartidos por login y registro."""
        self.email_label = tk.Label(
            self,
            text="Correo electrónico:",
            font=("Arial", 14),
            bg=BG,
        )
        self.email_label.pack(padx=10, pady=(10, 5))

        self.email_entry = self.create_entry()
        self.email_entry.pack(padx=10, pady=5)

        self.password_label = tk.Label(
            self,
            text="Contraseña:",
            font=("Arial", 14),
            bg=BG,
        )
        self.password_label.pack(padx=10, pady=(10, 5))

        self.password_entry = self.create_entry(show="*")
        self.password_entry.pack(padx=10, pady=5)

    def toggle_password(self):
        """Muestra u oculta la contraseña."""
        self.password_entry.config(
            show="" if self.show_password.get() else "*"
        )

    def add_show_password_checkbox(self):
        self.ck_box_show_password = tk.Checkbutton(
            self,
            text="Mostrar contraseña",
            variable=self.show_password,
            command=self.toggle_password,
            bg="white",
            activebackground="white",
            fg="black",
            activeforeground="black",
            selectcolor="white",
            highlightthickness=1,
            highlightbackground=cons.COLOR_BUTTON_GREEN,
            highlightcolor=cons.COLOR_BUTTON_GREEN_TEXT,
            bd=1,
            relief="solid",
            padx=8,
            pady=4,
        )
        self.ck_box_show_password.pack(padx=10, pady=5)


class LoginFormular(AccountsFormular):
    """Vista de inicio de sesión."""

    def build_widgets(self):
        super().build_widgets()

        self.add_show_password_checkbox()

        # Botón de login
        self.login_button = tk.Button(
            self,
            text="Iniciar sesión",
            width=18,
            command=self.login,
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        )
        self.login_button.pack(padx=10, pady=12)

        # Olvidé mi contraseña
        self.forgot_password_button = tk.Button(
            self,
            text="¿Olvidaste tu contraseña?",
            relief="flat",
            command=self.forgot_password_action,
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        )
        self.forgot_password_button.pack(padx=10, pady=5)

        # Ir a registro
        self.no_account_button = tk.Button(
            self,
            text="¿No tienes cuenta? Crear cuenta",
            relief="flat",
            command=lambda: self.controller.show_view("register"),
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        )
        self.no_account_button.pack(padx=10, pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()



        if not email or not password:
            messagebox.showwarning(
                "Campos incompletos",
                "Ingresa tu correo electrónico y contraseña.",
                parent=self,
            )
            return

        user = authenticate_mock(email, password)

        if user is None:
            messagebox.showerror(
                "Inicio de sesión fallido",
                "Correo electrónico o contraseña incorrectos.",
                parent=self,
            )
            return
        self.controller.current_user = user

        # Busca la persona ligada a la cuenta (misma db_id) en la "base de datos"
        # interna. Se guarda en el controller para que otras páginas la usen.
        self.controller.current_person = get_person_by_user(user)

        # TODO: agregar aquí la validación con la base de datos.
        # Mientras tanto el acceso es libre para poder probar la aplicación.

        # El dashboard recibe la cuenta y la persona activas para que la
        # barra superior muestre el nombre y el correo de quien inició sesión.
        DashboardFormular(
            self.controller,
            self.controller.current_user,
            self.controller.current_person,
        )

    def forgot_password_action(self):
        messagebox.showinfo(
            "Recuperar contraseña",
            "Agrega aquí el proceso para recuperar la contraseña.",
            parent=self,
        )


class RegisterFormular(AccountsFormular):
    """Vista de registro."""

    def build_widgets(self):
        # Nombre completo
        self.name_label = tk.Label(
            self,
            text="Nombre completo:",
            font=("Arial", 14),
            bg=BG,
        )
        self.name_label.pack(padx=10, pady=(10, 5))

        self.name_input = self.create_entry()
        self.name_input.pack(padx=10, pady=5)

        # Teléfono
        self.phone_label = tk.Label(
            self,
            text="Teléfono:",
            font=("Arial", 14),
            bg=BG,
        )
        self.phone_label.pack(padx=10, pady=(10, 5))

        self.phone_entry = self.create_entry()
        self.phone_entry.pack(padx=10, pady=5)

        # Correo y contraseña compartidos
        super().build_widgets()

        self.add_show_password_checkbox()

        # Botón de registro
        self.register_button = tk.Button(
            self,
            text="Crear cuenta",
            width=18,
            command=self.register,
        )
        self.register_button.pack(padx=10, pady=12)

        # ¿Ya tienes cuenta?
        self.account_already_button = tk.Button(
            self,
            text="¿Ya tienes cuenta? Iniciar sesión",
            relief="flat",
            command=lambda: self.controller.show_view("login"),
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
        )
        self.account_already_button.pack(padx=10, pady=5)

    def register(self):
        full_name = self.name_input.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not all((full_name, phone, email, password)):
            messagebox.showwarning(
                "Campos incompletos",
                "Completa todos los campos.",
                parent=self,
            )
            return

        self.is_institutional_email(email, full_name, phone)

    def is_institutional_email(self, email, full_name, phone):
        # Valida si el correo es institucional para guardarlo como tal en la BD.
        institutional_email = email.lower().endswith("@utr.edu.mx")

        if institutional_email:
            messagebox.showinfo(
                "Correo institucional",
                f"¡Cuenta creada!\nNombre: {full_name}\nCorreo: {email}",
                parent=self,
            )

            """
            MYSQL QUERY (Connection not yet implemented)
            INSERT INTO person (full_name, email, phone, institutional_email)
            VALUES ('full_name', 'email', 'phone', TRUE);
            SET @student_person_id = LAST_INSERT_ID();
            INSERT INTO account (person_id, password_hash)
            VALUES (@student_person_id, 'password');
            INSERT INTO student (person_id)
            VALUES (@student_person_id);
            """
        else:
            messagebox.showinfo(
                "Correo personal",
                f"¡Cuenta creada!\nNombre: {full_name}\nCorreo: {email}",
                parent=self,
            )

            """
            MYSQL QUERY (Connection not yet implemented)
            INSERT INTO person (full_name, email, phone, institutional_email)
            VALUES ('full_name', 'email', 'phone', FALSE);
            SET @student_person_id = LAST_INSERT_ID();
            INSERT INTO account (person_id, password_hash)
            VALUES (@student_person_id, 'password');
            INSERT INTO student (person_id)
            VALUES (@student_person_id);
            """