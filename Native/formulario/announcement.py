import tkinter as tk
from components.top_bar import TopBar
from components.left_menu import LeftMenu
import config.constants as cons

# Paleta de colores
COLOR_BG = "#F4F5F7"
COLOR_CARD_BG = "#FFFFFF"
COLOR_PRIMARY_GREEN = "#00A859"
COLOR_GREEN_HOVER = "#008F4C"
COLOR_TEXT_MAIN = "#2C3E50"
COLOR_TEXT_MUTED = "#666666"


class SeccionAnuncios(tk.Toplevel):
    def __init__(self, parent, user=None, person=None):
        super().__init__(parent, bg=COLOR_BG)
        self.user = user
        self.person = person
        self.images = []  # Referencia para conservar imágenes en memoria

        # Inicializamos los componentes base de la pantalla
        self.title("Anuncios")
        self.minsize(800, 450)
        self.configure(bg=cons.COLOR_BACKGROUND_SCREEN)
        self.build_components()

    def build_components(self):
        # Configurar la cuadrícula del Frame Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Barra Superior (TopBar)
        top_bar = TopBar(self, user=self.user, person=self.person)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # 2. Menú Lateral (LeftMenu)
        left_menu = LeftMenu(self, controller=self.master)
        left_menu.grid(row=1, column=0, sticky="ns")

        # 3. Área de Contenido Central
        content = tk.Frame(self, bg=COLOR_BG)
        content.grid(row=1, column=1, sticky="nsew")

        # Renderizar la sección de anuncios dentro del área de contenido
        self.build_widgets(content)

    def build_widgets(self, container):
        # ---------------------------------------------------------
        # 1. ENCABEZADO: Título "Anuncios" + Botón "+ Agregar anuncio"
        # ---------------------------------------------------------
        header_frame = tk.Frame(container, bg=COLOR_BG)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_title = tk.Label(
            header_frame,
            text="Anuncios",
            font=("Arial", 18, "bold"),
            bg=COLOR_BG,
            fg=COLOR_TEXT_MAIN,
            anchor="w"
        )
        lbl_title.pack(side="left")

        btn_add = tk.Button(
            header_frame,
            text="+ Agregar anuncio",
            font=("Arial", 10, "bold"),
            bg=COLOR_PRIMARY_GREEN,
            fg="white",
            activebackground=COLOR_GREEN_HOVER,
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.agregar_anuncio
        )
        btn_add.pack(side="right")

        # ---------------------------------------------------------
        # 2. DATOS DE LOS ANUNCIOS
        # ---------------------------------------------------------
        items = [
            {
                "title": "Donaciones de despensa",
                "description": "Te invitamos a participar en la campaña de donación de despensa para apoyar a familias de nuestra comunidad universitaria.",
                "date": "15 de abril de 2025",
                "image_route": "resources/placeholder.png",
                "command": lambda: self.ver_mas("Donaciones de despensa")
            },
            {
                "title": "Evento de vinculación",
                "description": "Acompáñanos en la Feria de Emprendedores, donde nuestros estudiantes presentarán sus proyectos e ideas de negocio.",
                "date": "28 de abril de 2025",
                "image_route": "resources/placeholder.png",
                "command": lambda: self.ver_mas("Evento de vinculación")
            }
        ]

        COLUMNS = 2
        current_row_frame = None

        # ---------------------------------------------------------
        # 3. RENDERIZADO DE LAS TARJETAS DENTRO DE `container`
        # ---------------------------------------------------------
        for index, item in enumerate(items):
            # Crea una fila nueva cada 2 tarjetas
            if index % COLUMNS == 0:
                current_row_frame = tk.Frame(container, bg=COLOR_BG)
                current_row_frame.pack(fill="x", padx=15, pady=8)

            image = tk.PhotoImage(file=item["image_route"])
            self.images.append(image)

            # Tarjeta blanca principal
            card = tk.Frame(
                current_row_frame,
                bg=COLOR_CARD_BG,
                highlightthickness=1,
                highlightbackground="#E2E8F0"
            )
            card.pack(side="left", fill="both", expand=True, padx=10)

            # A. Imagen superior
            lbl_image = tk.Label(
                card,
                image=image,
                bg=COLOR_CARD_BG
            )
            lbl_image.pack(fill="x", padx=12, pady=(12, 8))

            # B. Título
            lbl_card_title = tk.Label(
                card,
                text=item["title"],
                font=("Arial", 12, "bold"),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MAIN,
                anchor="w"
            )
            lbl_card_title.pack(fill="x", padx=12, pady=(4, 4))

            # C. Descripción (con ajuste automático multilínea)
            lbl_description = tk.Label(
                card,
                text=item["description"],
                font=("Arial", 9),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED,
                anchor="w",
                justify="left",
                wraplength=280
            )
            lbl_description.pack(fill="x", padx=12, pady=(0, 12))

            # D. Pie de la tarjeta
            footer_frame = tk.Frame(card, bg=COLOR_CARD_BG)
            footer_frame.pack(fill="x", padx=12, pady=(0, 12))

            lbl_date = tk.Label(
                footer_frame,
                text=f"{item['date']}",
                font=("Arial", 9),
                bg=COLOR_CARD_BG,
                fg=COLOR_TEXT_MUTED
            )
            lbl_date.pack(side="left", anchor="s")

            btn_ver_mas = tk.Button(
                footer_frame,
                text="Ver más",
                font=("Arial", 9, "bold"),
                bg=COLOR_PRIMARY_GREEN,
                fg="white",
                activebackground=COLOR_GREEN_HOVER,
                activeforeground="white",
                bd=0,
                padx=12,
                pady=4,
                cursor="hand2",
                command=item["command"]
            )
            btn_ver_mas.pack(side="right")

    # ---------------------------------------------------------
    # ACCIONES DE CALLBACK
    # ---------------------------------------------------------
    def agregar_anuncio(self):
        print("Abrir ventana modal para agregar nuevo anuncio...")

    def ver_mas(self, titulo_anuncio):
        print(f"Desplegando detalle de: {titulo_anuncio}")