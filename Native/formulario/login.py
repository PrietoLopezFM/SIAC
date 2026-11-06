import tkinter as tk
from tkinter import messagebox
from config import constants as cons
from util import util_window

class AccountsFormular(tk.Toplevel):
    """Base class for the login and registration windows."""

    def __init__(self, parent, title, width=370, height=570):
        super().__init__(parent)

        self.title(title)
        self.configure(bg=cons.C_DE_FONDO_LIGHT)
        self.attributes("-alpha", 0.96)

        util_window.centrar_ventana(self, width, height)

        self.show_password = tk.BooleanVar(value=False)
        self.build_widgets()

    def build_widgets(self):
        """Create fields shared by the login and registration forms."""
        self.email_label = tk.Label(
            self,
            text="Correo electrónico:",
            font=("Arial", 14),
            bg=cons.C_DE_FONDO_LIGHT,
        )
        self.email_label.pack(padx=10, pady=(20, 5))

        self.email_entry = tk.Entry(self, width=30,
            bg=cons.C_CAJA_TEXTO_LIGHT, fg=cons.C_CONTORNO_LIGHT)
        self.email_entry.pack(padx=10, pady=5)

        self.password_label = tk.Label(
            self,
            text="Contraseña:",
            font=("Arial", 14),
            bg=cons.C_DE_FONDO_LIGHT,
        )
        self.password_label.pack(padx=10, pady=(15, 5))

        self.password_entry = tk.Entry(self, width=30, show="*",
            bg=cons.C_CAJA_TEXTO_LIGHT, fg=cons.C_CONTORNO_LIGHT)
        self.password_entry.pack(padx=10, pady=5)

    def toggle_password(self):
        """Show or hide the password field."""
        self.password_entry.config(
            show="" if self.show_password.get() else "*"
        )

    def add_show_password_checkbox(self):
        # Show password checkbox
        self.ck_box_show_password = tk.Checkbutton(
            self,
            text="Mostrar contraseña",
            variable=self.show_password,
            command=self.toggle_password,
            bg=cons.C_DE_FONDO_LIGHT,
        )
        self.ck_box_show_password.pack(padx=10, pady=5)


class LoginFormular(AccountsFormular):
    """Login window."""

    def __init__(self, parent):
        super().__init__(parent, title="Login")

    def build_widgets(self):
        super().build_widgets()

        self.add_show_password_checkbox()

        # Login button
        self.login_button = tk.Button(
            self,
            text="Iniciar sesión",
            width=18,
            command=self.login,
            bg=cons.C_BOTONES_LIGHT
        )
        self.login_button.pack(padx=10, pady=15)

        # Forgot Password link
        self.forgot_password_button = tk.Button(
            self,
            text="¿Olvidaste tu contraseña?",
            relief="flat",
            command=self.forgot_password_action,
            bg=cons.C_BOTONES_LIGHT
        )
        self.forgot_password_button.pack(padx=10, pady=5)

        # No account button
        self.no_account_button = tk.Button(
            self,
            text="¿No tienes cuenta? Crear cuenta",
            relief="flat",
            command=self.open_register_form,
            bg=cons.C_BOTONES_LIGHT,
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

        # Add your login/database validation here.
        messagebox.showinfo(
            "Login",
            f"Se ingresó el correo: {email}",
            parent=self,
        )

    def forgot_password_action(self):
        messagebox.showinfo(
            "Recuperar contraseña",
            "Agrega aquí el proceso para recuperar la contraseña.",
            parent=self,
        )

    def open_register_form(self):
        parent = self.master
        self.destroy()
        RegisterFormular(parent)


class RegisterFormular(AccountsFormular):
    """Registration window."""

    def __init__(self, parent):
        super().__init__(parent, title="Registro", width=370, height=700)

    def build_widgets(self):
        # Full name input
        self.name_label = tk.Label(
            self,
            text="Nombre completo:",
            font=("Arial", 14),
            bg=cons.C_DE_FONDO_LIGHT,
        )
        self.name_label.pack(padx=10, pady=(20, 5))

        self.name_input = tk.Entry(self, width=30)
        self.name_input.pack(padx=10, pady=5)

        # Phone input
        self.phone_label = tk.Label(
            self,
            text="Teléfono:",
            font=("Arial", 14),
            bg=cons.C_DE_FONDO_LIGHT,
        )
        self.phone_label.pack(padx=10, pady=(15, 5))

        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.pack(padx=10, pady=5)

        # Shared email and password inputs
        super().build_widgets()

        self.add_show_password_checkbox()

        # Register button
        self.register_button = tk.Button(
            self,
            text="Crear cuenta",
            width=18,
            command=self.register,
        )
        self.register_button.pack(padx=10, pady=15)

        # Already have an account? button
        self.account_already_button = tk.Button(
            self,
            text="¿Ya tienes cuenta? Iniciar sesión",
            relief="flat",
            command=self.open_login_form,
            bg=cons.C_BOTONES_LIGHT,
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
        # Validate if the email is an institutional one to store it as such in the database.
        institutional_email = email.lower().endswith("@utr.edu.mx")

        if institutional_email:
            # Is an institutional email
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
            # Is a personal email
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

    def open_login_form(self):
        parent = self.master
        self.destroy()
        LoginFormular(parent)