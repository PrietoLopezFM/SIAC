import tkinter as tk

from config.constants import COLOR_BACKGROUND_SECONDARY_RED


class TopBar(tk.Frame):
    def __init__(self, parent, user, person):
        super().__init__(parent, bg=COLOR_BACKGROUND_SECONDARY_RED)

        self.user = user
        self.person = person
        self.images = []  # Keep image references alive.

        self.build_widgets()
        self.update_user_menu()

    def load_image(self, path):
        image = tk.PhotoImage(file=path)
        self.images.append(image)
        return image

    def build_widgets(self):
        self.configure(height=70)
        self.grid_columnconfigure(2, weight=1)

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

        # App title
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

        # User button
        user_icon = self.load_image("resources/placeholder.png")

        self.user_button = tk.Button(
            self,
            image=user_icon,
            compound="top",
            command=self.show_user_menu,
            relief="flat",
            bg=COLOR_BACKGROUND_SECONDARY_RED,
            fg="white",
            activebackground=COLOR_BACKGROUND_SECONDARY_RED,
            activeforeground="white",
        )
        self.user_button.grid(row=0, column=3, padx=15)

        # User menu
        self.user_menu = tk.Menu(self, tearoff=False, bg="white", fg="black")
        self.user_menu.add_command(label="", state="disabled")
        self.user_menu.add_command(label="", state="disabled")

    def update_user_menu(self):
        """Update the button and menu using the supplied account and person."""
        self.user_button.configure(text=f"{self.person.full_name}  ∨")
        self.user_menu.entryconfigure(0, label=self.person.full_name)

        # Use the account email for the logged-in account.
        self.user_menu.entryconfigure(1, label=self.user.email)

    def show_user_menu(self):
        self.user_menu.tk_popup(
            self.user_button.winfo_rootx(),
            self.user_button.winfo_rooty() + self.user_button.winfo_height(),
        )
