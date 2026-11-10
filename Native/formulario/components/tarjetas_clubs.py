import tkinter as tk

# Puedes usar tus constantes de color del proyecto
COLOR_BG = "#F4F5F7"
COLOR_CARD_BG = "#FFFFFF"
COLOR_TEXT_RED = "#B30000"
COLOR_TEXT_DARK = "#333333"
COLOR_BADGE_BG = "#00A859"
COLOR_BADGE_FG = "#FFFFFF"


class PanelPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.build_widgets()

    def build_widgets(self):
        # 1. Título de la sección
        lbl_title = tk.Label(
            self,
            text="Panel Principal",
            font=("Arial", 18, "bold"),
            bg=COLOR_BG,
            fg="#2C3E50",
            anchor="w"
        )
        lbl_title.pack(fill="x", padx=20, pady=(15, 10))

        # 2. Datos de los clubes según la imagen
        items = [
            {
                "title": "Club: Ajedrez",
                "image_route": "resources/placeholder.png",
                "students": "45 alumnos",
                "schedule": "Horario: Mar - Jue",
                "command": lambda: self.open_club("Ajedrez")
            },
            {
                "title": "Club: Fútbol",
                "image_route": "resources/placeholder.png",
                "students": "45 alumnos",
                "schedule": "Horario: Lun-Mié-Vie 4-6",
                "command": lambda: self.open_club("Fútbol")
            },
            {
                "title": "Club: Voleibol",
                "image_route": "resources/placeholder.png",
                "students": "40 alumnos",
                "schedule": "Horario: Mar - Jue 3-5",
                "command": lambda: self.open_club("Voleibol")
            },
            {
                "title": "Club: Gym",
                "image_route": "resources/placeholder.png",
                "students": "40 alumnos",
                "schedule": "Horario: Lun - Vie 2-6",
                "command": lambda: self.open_club("Gym")
            },
            {
                "title": "Club: Lectura",
                "image_route": "resources/placeholder.png",
                "students": "20 alumnos",
                "schedule": "Horario: Viernes 1-2 pm",
                "command": lambda: self.open_club("Lectura")
            },
            {
                "title": "Club: Básquetbol",
                "image_route": "resources/placeholder.png",
                "students": "45 alumnos",
                "schedule": "Horario: Lun - Mié 4-6",
                "command": lambda: self.open_club("Básquetbol")
            },
        ]

        self.images = []
        COLUMNS = 3
        current_row_frame = None

        # 3. Creación de la retícula (2 filas x 3 columnas)
        for index, item in enumerate(items):
            if index % COLUMNS == 0:
                current_row_frame = tk.Frame(self, bg=COLOR_BG)
                current_row_frame.pack(fill="x", padx=15, pady=8)

            image = tk.PhotoImage(file=item["image_route"])
            self.images.append(image)

            # Tarjeta Contenedora (Frame cliqueable)
            card = tk.Frame(
                current_row_frame,
                bg=COLOR_CARD_BG,
                highlightthickness=1,
                highlightbackground="#E2E8F0", # Borde suave alrededor de la tarjeta
                cursor="hand2"
            )
            card.pack(side="left", fill="both", expand=True, padx=8)

            # A. Título en color rojo (Club: XXX)
            lbl_card_title = tk.Label(
                card,
                text=item["title"],
                font=("Arial", 12, "bold"),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_RED,
                anchor="w"
            )
            lbl_card_title.pack(fill="x", padx=12, pady=(12, 6))

            # B. Imagen central
            lbl_image = tk.Label(
                card,
                image=image,
                bg=COLOR_CARD_BG
            )
            lbl_image.pack(padx=12, pady=4)

            # C. Fila de la etiqueta "Info: 45 alumnos"
            info_frame = tk.Frame(card, bg=COLOR_CARD_BG)
            info_frame.pack(fill="x", padx=12, pady=(6, 2))

            lbl_info_text = tk.Label(
                info_frame,
                text="Info: ",
                font=("Arial", 9),
                bg=COLOR_CARD_BG,
                fg="#666666"
            )
            lbl_info_text.pack(side="left")

            # Etiqueta verde (Badge de alumnos)
            lbl_badge = tk.Label(
                info_frame,
                text=item["students"],
                font=("Arial", 8, "bold"),
                bg=COLOR_BADGE_BG,
                fg=COLOR_BADGE_FG,
                padx=8,
                pady=2
            )
            lbl_badge.pack(side="left")

            # D. Texto del Horario
            lbl_schedule = tk.Label(
                card,
                text=item["schedule"],
                font=("Arial", 9),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_DARK,
                anchor="w"
            )
            lbl_schedule.pack(fill="x", padx=12, pady=(2, 12))

            # 4. Asignar el clic del ratón (Acción de botón) a todos los elementos internos
            elements = [card, lbl_card_title, lbl_image, info_frame, lbl_info_text, lbl_badge, lbl_schedule]
            for element in elements:
                element.bind("<Button-1>", lambda e, cmd=item["command"]: cmd())

    def open_club(self, club_name):
        print(f"Abriendo el módulo del {club_name}...")