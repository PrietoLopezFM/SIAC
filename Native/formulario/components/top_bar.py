import tkinter as tk

from config.constants import COLOR_BACKGROUND_SECONDARY_RED


class TopBar(tk.Frame):
    def __init__(
        self,
        parent,
        user_name="Admin",
        user_email="admin@example.com",
    ):
        super().__init__(parent, bg=COLOR_BACKGROUND_SECONDARY_RED)
        self.user_name = user_name
        self.user_email = user_email
        self.images = []  # Keep image references alive.
        self.build_widgets()

    def load_image(self, path):
        image = tk.PhotoImage(file=path)
        self.images.append(image)
        return image

    def build_widgets(self):
        self.configure(height=70)
        self.grid_columnconfigure(1, weight=1)

        # Logos
        utr_logo = self.load_image("resources/placeholder.png")
        wildcats_logo = self.load_image("resources/placeholder.png")

        tk.Label(
            self,
            image=utr_logo,
            bg=COLOR_BACKGROUND_SECONDARY_RED,
        ).grid(row=0, column=0, padx=(10, 5))

        tk.Label(
            self,
            image=wildcats_logo,
            bg=COLOR_BACKGROUND_SECONDARY_RED,
        ).grid(row=0, column=1, padx=5)

        # App name and full name, stacked vertically
        title_frame = tk.Frame(self, bg=COLOR_BACKGROUND_SECONDARY_RED)
        title_frame.grid(row=0, column=2, sticky="w", padx=10)

        tk.Label(
            title_frame,
            text="SIAC",
            font=("Arial", 16, "bold"),
            bg=COLOR_BACKGROUND_SECONDARY_RED,
            fg="white",
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Sistema Integrado de Asistencias y Creditos",
            font=("Arial", 9),
            bg=COLOR_BACKGROUND_SECONDARY_RED,
            fg="white",
        ).pack(anchor="w")

        # User button and dropdown menu
        user_icon = self.load_image("resources/placeholder.png")

        user_button = tk.Button(
            self,
            text=f"{self.user_name}  ∨",
            image=user_icon,
            compound="top",
            command=self.show_user_menu,
            relief="flat",
            bg=COLOR_BACKGROUND_SECONDARY_RED,
            fg="white",
            activebackground=COLOR_BACKGROUND_SECONDARY_RED,
            activeforeground="white",
        )
        user_button.grid(row=0, column=3, padx=15)

        self.user_menu = tk.Menu(
            self,
            tearoff=False,
            bg="white",
            fg="black",
        )
        self.user_menu.add_command(label=self.user_name, state="disabled")
        self.user_menu.add_command(label=self.user_email, state="disabled")

    def show_user_menu(self):
        button = self.grid_slaves(row=0, column=3)[0]
        self.user_menu.tk_popup(
            button.winfo_rootx(),
            button.winfo_rooty() + button.winfo_height(),
        )
