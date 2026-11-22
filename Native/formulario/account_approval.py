import tkinter as tk
from tkinter import messagebox

from components.left_menu import LeftMenu
from components.top_bar import TopBar
from database.connection import start_connection
from database.queries import get_accounts_by_status, approve_account


BG = "#F4F5F7"
TEXT = "#2C3E50"


class AccountApproval(tk.Toplevel):
    def __init__(self, parent, user, person):
        super().__init__(parent)
        self.user = user
        self.person = person
        self.current_role = None
        self.sections = []
        self.role_card_images = []

        self.title("Aprobar Cuentas")
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
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._show_role_menu()

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _show_role_menu(self):
        self.current_role = None
        self.sections = []
        self._clear_content()

        frame = tk.Frame(self.content, bg=BG)
        frame.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(
            frame,
            text="APROBAR CUENTAS",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        tk.Label(
            frame,
            text="Selecciona el tipo de cuenta que quieres revisar.",
            font=("Segoe UI", 10),
            bg=BG,
            fg="#666666",
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 22))

        cards_frame = tk.Frame(frame, bg=BG)
        cards_frame.grid(row=2, column=0, sticky="ew")

        for column in range(3):
            cards_frame.grid_columnconfigure(column, weight=1)

        items = [
            ("student", "Estudiantes",
             "Revisar cuentas pendientes y aprobadas de estudiantes."),
            ("administrator", "Administradores",
             "Revisar cuentas pendientes y aprobadas de administradores."),
            ("instructor", "Instructores",
             "Revisar cuentas pendientes y aprobadas de instructores."),
        ]

        for index, (role, title_text, description_text) in enumerate(items):
            image = tk.PhotoImage(file="resources/placeholder.png")
            hover_image = tk.PhotoImage(file="resources/placeholder.png")
            self.role_card_images.extend((image, hover_image))

            card = tk.Frame(
                cards_frame,
                bg="#FFFFFF",
                highlightthickness=1,
                highlightbackground="#E2E8F0",
                cursor="hand2",
                height=220,
            )
            card.grid(row=0, column=index, sticky="nsew", padx=8, pady=8)
            card.grid_propagate(False)

            icon = tk.Label(card, image=image, bg="#FFFFFF", cursor="hand2")
            icon.pack(pady=(22, 12))

            title = tk.Label(
                card,
                text=title_text,
                font=("Segoe UI", 12, "bold"),
                bg="#FFFFFF",
                fg=TEXT,
                cursor="hand2",
            )
            title.pack(pady=(0, 8))

            description = tk.Label(
                card,
                text=description_text,
                font=("Segoe UI", 9),
                bg="#FFFFFF",
                fg="#666666",
                justify="center",
                wraplength=240,
                cursor="hand2",
            )
            description.pack(padx=16)

            command = lambda selected_role=role: self._show_role(selected_role)
            for widget in (card, icon, title, description):
                widget.bind("<Button-1>", lambda _event, cmd=command: cmd())
                widget.bind(
                    "<Enter>",
                    lambda _event, c=card, i=icon, img=hover_image:
                        self._set_role_card_hover(c, i, img, True),
                )
                widget.bind(
                    "<Leave>",
                    lambda _event, c=card, i=icon, img=image:
                        self._set_role_card_hover(c, i, img, False),
                )

    def _set_role_card_hover(self, card, icon, image, hovering):
        bg = "#F0FDF4" if hovering else "#FFFFFF"
        border = "#00A859" if hovering else "#E2E8F0"

        card.configure(bg=bg, highlightbackground=border)
        for child in card.winfo_children():
            child.configure(bg=bg)
        icon.configure(image=image)

    def _show_role(self, role):
        self.current_role = role
        self.sections = []
        self._clear_content()

        frame = tk.Frame(self.content, bg=BG)
        frame.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        header = tk.Frame(frame, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.grid_columnconfigure(1, weight=1)

        tk.Button(
            header,
            text="← Back",
            command=self._show_role_menu,
            cursor="hand2",
        ).grid(row=0, column=0, sticky="w", padx=(0, 14))

        role_title = {
            "student": "Estudiantes",
            "administrator": "Administradores",
            "instructor": "Instructores",
        }.get(role, "Cuentas")

        tk.Label(
            header,
            text=f"APROBAR CUENTAS: {role_title.upper()}",
            font=("Segoe UI", 16, "bold"),
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).grid(row=0, column=1, sticky="ew")

        search_frame = tk.Frame(frame, bg=BG)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        search_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            search_frame,
            text="Buscar:",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._refresh_sections)

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
        ).grid(row=0, column=1, sticky="ew")

        self.sections_frame = tk.Frame(frame, bg=BG)
        self.sections_frame.grid(row=2, column=0, sticky="nsew")

        self._load_role_accounts()

    def _load_role_accounts(self):
        connection = None
        cursor = None

        try:
            connection = start_connection()
            cursor = connection.cursor()

            pending = get_accounts_by_status(
                cursor, self.current_role, "pending"
            )
            approved = get_accounts_by_status(
                cursor, self.current_role, "approved"
            )

            self.sections = [
                {"title": "Pending Approval", "rows": pending, "pending": True},
                {"title": "Approved Accounts", "rows": approved, "pending": False},
            ]
            self._refresh_sections()

        except Exception as error:
            messagebox.showerror(
                "Aprobar Cuentas",
                f"No se pudieron cargar las cuentas:\n{error}",
                parent=self,
            )
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def _refresh_sections(self, *_):
        if not hasattr(self, "sections_frame"):
            return

        for widget in self.sections_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().strip().casefold()

        for section in self.sections:
            outer = tk.Frame(self.sections_frame, bg=BG)
            outer.pack(fill="x", pady=6)

            body = tk.Frame(outer, bg="white")
            body.pack(fill="x")

            expanded = {"value": True}
            title = section["title"]

            toggle_button = tk.Button(
                outer,
                text=f"▼ {title}",
                anchor="w",
                bg="#E6E9ED",
                relief="flat",
                cursor="hand2",
            )

            def toggle(section_body=body, state=expanded, button=toggle_button,
                       section_title=title):
                if state["value"]:
                    section_body.pack_forget()
                    state["value"] = False
                    button.configure(text=f"▶ {section_title}")
                else:
                    section_body.pack(fill="x")
                    state["value"] = True
                    button.configure(text=f"▼ {section_title}")

            toggle_button.configure(command=toggle)
            toggle_button.pack(fill="x")

            rows = [
                row for row in section["rows"]
                if not query or any(
                    query in str(value or "").casefold()
                    for value in row[1:]
                )
            ]
            self._draw_table(body, rows, section["pending"])

    def _draw_table(self, parent, rows, pending):
        headings = ["Full name", "Email", "Phone", "Email type"]
        if pending:
            headings.append("Action")
        else:
            headings.extend(["Approved at", "Approved by"])

        table = tk.Frame(parent, bg="white")
        table.pack(fill="x", padx=8, pady=8)

        for column, heading in enumerate(headings):
            table.grid_columnconfigure(column, weight=1)
            tk.Label(
                table,
                text=heading,
                font=("Segoe UI", 9, "bold"),
                bg="#E6E9ED",
                anchor="w",
                padx=6,
                pady=6,
            ).grid(row=0, column=column, sticky="ew")

        if not rows:
            tk.Label(
                table,
                text="No accounts to show.",
                bg="white",
                anchor="w",
                padx=6,
                pady=8,
            ).grid(
                row=1, column=0, columnspan=len(headings), sticky="ew"
            )
            return

        for row_index, row in enumerate(rows, start=1):
            # Row: person_id, name, email, phone, email_type,
            # approved_at, approved_by
            values = [row[1], row[2], row[3] or "—", row[4]]

            if not pending:
                values.extend([row[5] or "—", row[6] or "—"])

            for column, value in enumerate(values):
                tk.Label(
                    table,
                    text=str(value or "—"),
                    bg="white",
                    anchor="w",
                    padx=6,
                    pady=6,
                ).grid(row=row_index, column=column, sticky="ew")

            if pending:
                tk.Button(
                    table,
                    text="Approve",
                    cursor="hand2",
                    command=lambda person_id=row[0]:
                        self._approve(person_id),
                ).grid(row=row_index, column=4, padx=6, pady=4)

    def _approve(self, person_id):
        # Approval records the administrator's person db_id.
        admin_person_id = getattr(self.person, "db_id", None)
        if admin_person_id is None:
            admin_person_id = getattr(self.user, "db_id", None)

        if admin_person_id is None:
            messagebox.showerror(
                "Aprobar cuenta",
                "No se encontró el ID del administrador que inició sesión.",
                parent=self,
            )
            return

        connection = None
        cursor = None

        try:
            connection = start_connection()
            cursor = connection.cursor()

            updated = approve_account(
                cursor,
                person_id,
                admin_person_id,
                self.current_role,
            )
            connection.commit()

            if updated:
                self._load_role_accounts()
            else:
                messagebox.showwarning(
                    "Aprobar cuenta",
                    "La cuenta no se aprobó. Puede que ya esté aprobada "
                    "o que el usuario actual no sea administrador.",
                    parent=self,
                )

        except Exception as error:
            if connection is not None:
                connection.rollback()
            messagebox.showerror(
                "Aprobar cuenta",
                f"No se pudo aprobar la cuenta:\n{error}",
                parent=self,
            )
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
