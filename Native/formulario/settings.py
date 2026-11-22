import tkinter as tk
from tkinter import messagebox, ttk

from components.left_menu import LeftMenu
from components.top_bar import TopBar
from database.connection import start_connection
from database.queries import update_person_data


BG = "#F4F5F7"
TEXT = "#2C3E50"


class SettingsPage(tk.Toplevel):
    def __init__(self, parent, user, person):
        super().__init__(parent)
        self.user = user
        self.person = person

        self.title("Configuración")
        self.geometry("1100x700")
        self.minsize(800, 450)
        self.configure(bg=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        TopBar(self, user=user, person=person).grid(
            row=0, column=0, columnspan=2, sticky="ew"
        )
        LeftMenu(self, controller=self.master).grid(
            row=1, column=0, sticky="ns"
        )

        self.content = tk.Frame(self, bg=BG)
        self.content.grid(row=1, column=1, sticky="nsew", padx=28, pady=24)
        self.content.grid_columnconfigure(0, weight=1)

        self._build_page()

    @staticmethod
    def _email_type_for(email):
        if email.strip().lower().endswith("@utr.edu.mx"):
            return "institutional"
        return "personal"

    def _build_page(self):
        tk.Label(
            self.content,
            text="CONFIGURACIÓN",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 20))

        profile = tk.LabelFrame(
            self.content,
            text="Datos personales",
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=TEXT,
            padx=18,
            pady=16,
        )
        profile.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        profile.grid_columnconfigure(1, weight=1)

        self.name_var = tk.StringVar(value=self.person.full_name or "")
        self.email_var = tk.StringVar(value=self.person.email or "")
        self.phone_var = tk.StringVar(value=self.person.phone or "")
        self.email_type_var = tk.StringVar(
            value=self._email_type_for(self.person.email or "")
        )

        self._add_entry(profile, 0, "Nombre completo", self.name_var)
        self._add_entry(profile, 1, "Correo electrónico", self.email_var)
        self._add_entry(profile, 2, "Teléfono", self.phone_var)

        tk.Label(
            profile,
            text="Tipo de correo",
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=3, column=0, sticky="w", padx=(0, 16), pady=8)

        tk.Label(
            profile,
            textvariable=self.email_type_var,
            bg=BG,
            fg="#555555",
            anchor="w",
        ).grid(row=3, column=1, sticky="w", pady=8)

        self.email_var.trace_add("write", self._update_email_type)

        preferences = tk.LabelFrame(
            self.content,
            text="Preferencias",
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=TEXT,
            padx=18,
            pady=16,
        )
        preferences.grid(row=2, column=0, sticky="ew", pady=(0, 18))
        preferences.grid_columnconfigure(1, weight=1)

        tk.Label(
            preferences,
            text="Tema",
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(0, 16), pady=8)

        self.theme_var = tk.StringVar(value="Predeterminado")
        ttk.Combobox(
            preferences,
            textvariable=self.theme_var,
            values=("Predeterminado", "Claro", "Oscuro"),
            state="readonly",
        ).grid(row=0, column=1, sticky="ew", pady=8)

        tk.Label(
            preferences,
            text="Idioma",
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=(0, 16), pady=8)

        self.language_var = tk.StringVar(value="Español")
        ttk.Combobox(
            preferences,
            textvariable=self.language_var,
            values=("Español", "English"),
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", pady=8)

        tk.Button(
            self.content,
            text="Guardar cambios",
            command=self._save_changes,
            cursor="hand2",
            bg="#00A859",
            fg="white",
            activebackground="#008F4C",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=8,
        ).grid(row=3, column=0, sticky="e")

    @staticmethod
    def _add_entry(parent, row, label_text, variable):
        tk.Label(
            parent,
            text=label_text,
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=row, column=0, sticky="w", padx=(0, 16), pady=8)

        tk.Entry(
            parent,
            textvariable=variable,
        ).grid(row=row, column=1, sticky="ew", pady=8)

    def _update_email_type(self, *_):
        self.email_type_var.set(self._email_type_for(self.email_var.get()))

    def _save_changes(self):
        full_name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        email_type = self._email_type_for(email)

        if not full_name:
            messagebox.showwarning(
                "Configuración",
                "El nombre completo es obligatorio.",
                parent=self,
            )
            return

        if not email:
            messagebox.showwarning(
                "Configuración",
                "El correo electrónico es obligatorio.",
                parent=self,
            )
            return

        connection = None
        cursor = None

        try:
            connection = start_connection()
            cursor = connection.cursor()

            update_person_data(
                cursor,
                self.person.db_id,
                full_name,
                email,
                phone or None,
                email_type,
            )
            connection.commit()

            # Keep the in-memory model in sync with the database.
            self.person.full_name = full_name
            self.person.email = email
            self.person.phone = phone or None
            self.person.email_type = email_type

            messagebox.showinfo(
                "Configuración",
                "Los cambios se guardaron correctamente.",
                parent=self,
            )

        except Exception as error:
            if connection is not None:
                connection.rollback()

            messagebox.showerror(
                "Configuración",
                f"No se pudieron guardar los cambios:\n{error}",
                parent=self,
            )
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
