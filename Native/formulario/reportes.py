import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from components.left_menu import LeftMenu
from components.top_bar import TopBar
from config import constants as cons
from models import get_students


def get_report_rows(periods):
    """Build the table rows from the students in the database (mock for now).

    Only students are listed (no administrators nor instructors).
    periods: the period headings (e.g. "Sep-Dic 2026"); each one shows the
             club the student had in that period, or '-' if none.
    Each row follows the order of ReportesFormular.columns.
    """
    rows = []

    for student in get_students():
        rows.append((
            student.student_number,
            student.full_name,
            *(student.club_history.get(period, "-") for period in periods),
            f"{student.credits}/100",  # Total Creditos: shown as 'X/100'
        ))

    return rows


class ReportesFormular(tk.Toplevel):
    def __init__(self, parent, user, person):
        super().__init__(parent)
        self.user = user
        self.person = person

        self.title("Reportes")
        self.minsize(800, 450)
        self.configure(bg=cons.COLOR_BACKGROUND_SCREEN)

        self.columns = (
            "ID",
            "Nombre completo",
            # The period information will ome from the database when implemented, for now it can stay static
            "Sep-Dic 2026", #placeholder Futbol
            "Ene-Abr 2026", #placeholder Club de Lectura
            "May-Ago 2026", #placeholder Ajedrez
            "Total Creditos", # green, rounded, white bold font
        )

        # Each student entry is a new row here because of all the data shown.
        # Replace with data from your database when available.
        # Each row must match the order of self.columns.
        # The three period headings (columns 2 to 4) tell which clubs to show.
        self.rows = get_report_rows(self.columns[2:5])

        self.build_components()

    def build_components(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top_bar = TopBar(self, user=self.user, person=self.person)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        left_menu = LeftMenu(self, controller=self.master)
        left_menu.grid(row=1, column=0, sticky="ns")

        content = tk.Frame(self, bg=cons.COLOR_BACKGROUND_SCREEN)
        content.grid(row=1, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        # Title and controls share the same header row.
        header = tk.Frame(content, bg=cons.COLOR_BACKGROUND_SCREEN)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        tk.Label(
            header,
            text="REPORTES",
            font=("Segoe UI", 16, "bold"),
            bg=cons.COLOR_BACKGROUND_SCREEN,
            fg=cons.COLOR_SCREEN_TEXT,
        ).grid(row=0, column=0, sticky="w")

        self.build_widgets(content, header)

    def build_widgets(self, parent, header):
        controls = tk.Frame(header, bg=cons.COLOR_BACKGROUND_SCREEN)
        controls.grid(row=0, column=1, sticky="e", padx=(20, 0))
        controls.grid_columnconfigure(1, weight=1)

        tk.Label(
            controls,
            text="Búsqueda:",
            bg=cons.COLOR_BACKGROUND_SCREEN,
            fg=cons.COLOR_SCREEN_TEXT,
        ).grid(row=0, column=0, sticky="w")

        self.search_var = tk.StringVar()
        # Search field uses the same style as the login fields.
        search_entry = tk.Entry(
            controls,
            textvariable=self.search_var,
            width=24,
            bg=cons.COLOR_BACKGROUND_ELEMENTS,
            fg=cons.COLOR_INPUT_TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=cons.COLOR_BORDER_ELEMENTS,  # borde sin foco
            highlightcolor=cons.COLOR_BORDER_ELEMENTS,       # borde con foco
        )
        search_entry.grid(row=0, column=1, sticky="ew", padx=(8, 10))

        tk.Button(
            controls,
            text="Exportar CSV",
            command=self.export_csv,
            bg=cons.COLOR_BUTTON_GREEN,
            fg=cons.COLOR_BUTTON_GREEN_TEXT,
            activebackground=cons.COLOR_BUTTON_GREEN,
            activeforeground=cons.COLOR_BUTTON_GREEN_TEXT,
        ).grid(row=0, column=2, sticky="e")

        # The table is placed below the header.
        table_frame = tk.Frame(parent, bg=cons.COLOR_BACKGROUND_SCREEN)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            table_frame,
            bg=cons.COLOR_BACKGROUND_REPORTES_TABLE,
            highlightthickness=0,
        )
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        vertical_scrollbar = tk.Scrollbar(
            table_frame, orient="vertical", command=self.canvas.yview
        )
        horizontal_scrollbar = tk.Scrollbar(
            table_frame, orient="horizontal", command=self.canvas.xview
        )

        self.canvas.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        # One width per column in self.columns.
        self.column_widths = (65, 210, 130, 130, 130, 120)
        self.header_height = 38
        self.row_height = 42

        self.search_var.trace_add("write", self.draw_table)
        self.draw_table()

    def get_filtered_rows(self):
        query = self.search_var.get().strip().casefold()
        if not query:
            return self.rows

        return [
            row for row in self.rows
            if any(query in str(value).casefold() for value in row)
        ]

    def rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1,
        ]
        return self.canvas.create_polygon(
            points, smooth=True, splinesteps=12, **kwargs
        )

    def draw_table(self, *_):
        self.canvas.delete("all")
        filtered_rows = self.get_filtered_rows()

        x_positions = [0]
        for width in self.column_widths:
            x_positions.append(x_positions[-1] + width)

        # Header
        for i, heading in enumerate(self.columns):
            x1, x2 = x_positions[i], x_positions[i + 1]
            self.canvas.create_rectangle(
                x1, 0, x2, self.header_height,
                fill=cons.COLOR_REPORTES_TABLE_HEADER,
                outline=cons.COLOR_REPORTES_TABLE_SEPARATION,
            )
            self.canvas.create_text(
                x1 + 8,
                self.header_height / 2,
                text=heading,
                anchor="w",
                fill=cons.COLOR_REPORTES_TABLE_HEADER_TEXT,
                font=("Segoe UI", 9, "bold"),
            )

        # Student rows
        for row_index, row in enumerate(filtered_rows):
            y1 = self.header_height + row_index * self.row_height
            y2 = y1 + self.row_height
            # Reportes rows share one background (no alternating colors).
            row_bg = cons.COLOR_BACKGROUND_REPORTES_TABLE

            self.canvas.create_rectangle(
                0, y1, x_positions[-1], y2,
                fill=row_bg,
                outline="",
            )
            # Thin line separating this row from the next one.
            self.canvas.create_line(
                0, y2, x_positions[-1], y2,
                fill=cons.COLOR_REPORTES_TABLE_SEPARATION,
            )

            for column_index, value in enumerate(row):
                x1, x2 = x_positions[column_index], x_positions[column_index + 1]

                if column_index == 5:  # Total Creditos: green badge
                    badge_x1 = x1 + 8
                    badge_x2 = x2 - 8
                    badge_y1 = y1 + 7
                    badge_y2 = y2 - 7
                    self.rounded_rect(
                        badge_x1, badge_y1, badge_x2, badge_y2, 10,
                        fill=cons.COLOR_BUTTON_GREEN,
                        outline="",
                    )
                    self.canvas.create_text(
                        (badge_x1 + badge_x2) / 2,
                        (y1 + y2) / 2,
                        text=str(value),
                        fill=cons.COLOR_BUTTON_GREEN_TEXT,
                        font=("Segoe UI", 9, "bold"),
                    )
                else:
                    self.canvas.create_text(
                        x1 + 8,
                        (y1 + y2) / 2,
                        text=str(value),
                        anchor="w",
                        fill=cons.COLOR_REPORTES_TABLE_TEXT,
                        font=("Segoe UI", 9),
                    )

        if not filtered_rows:
            message = "No hay estudiantes para mostrar."
            if self.rows:
                message = "No se encontraron estudiantes."

            self.canvas.create_text(
                10,
                self.header_height + 20,
                text=message,
                anchor="w",
                fill=cons.COLOR_REPORTES_TABLE_TEXT,
                font=("Segoe UI", 10),
            )

        content_height = self.header_height + max(len(filtered_rows), 1) * self.row_height
        self.canvas.configure(
            scrollregion=(0, 0, sum(self.column_widths), content_height)
        )

    def on_canvas_resize(self, event):
        # Keep the existing proportions, but scale them to fit the canvas.
        base_widths = (65, 210, 130, 130, 130, 120)
        total_base_width = sum(base_widths)
        available_width = max(event.width, total_base_width)

        self.column_widths = [
            round(width * available_width / total_base_width)
            for width in base_widths
        ]

        self.draw_table()

    def export_csv(self):
        filtered_rows = self.get_filtered_rows()
        if not filtered_rows:
            messagebox.showinfo(
                "Exportar CSV",
                "No hay estudiantes para exportar.",
                parent=self,
            )
            return

        filename = filedialog.asksaveasfilename(
            parent=self,
            title="Guardar estudiantes como CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not filename:
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(self.columns)
                writer.writerows(filtered_rows)

            messagebox.showinfo(
                "Exportar CSV",
                "El archivo CSV se guardó correctamente.",
                parent=self,
            )
        except OSError as error:
            messagebox.showerror(
                "Exportar CSV",
                f"No se pudo guardar el archivo:\n{error}",
                parent=self,
            )