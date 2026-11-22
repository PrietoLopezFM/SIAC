import tkinter as tk
from tkinter import messagebox

from components.left_menu import LeftMenu
from components.top_bar import TopBar
from components.activity_slide import ActivitySlide

from database.connection import start_connection
from database.queries import get_activity_offerings
from models.offering import Offering


class ActivitiesPage(tk.Toplevel):
    def __init__(self, parent, user, person):
        super().__init__(parent)
        self.user = user
        self.person = person
        self.title("Activities")
        self.geometry("1000x700")

        self.activities = []
        self._build_components()
        self._load_activities()

    def _build_components(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top_bar = TopBar(self, user=self.user, person=self.person)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        left_menu = LeftMenu(self, controller=self.master)
        left_menu.grid(row=1, column=0, sticky="ns")

        content = tk.Frame(self, bg="#F4F5F7")
        content.grid(row=1, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        toolbar = tk.Frame(content, bg="#F4F5F7")
        toolbar.grid(row=0, column=0, sticky="ew", padx=20, pady=16)
        toolbar.grid_columnconfigure(1, weight=1)

        tk.Label(
            toolbar,
            text="Activities",
            font=("Arial", 18, "bold"),
            bg="#F4F5F7",
            fg="#2C3E50",
        ).grid(row=0, column=0, padx=(0, 18))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(toolbar, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        search_entry.bind("<KeyRelease>", self._search_activities)

        tk.Button(
            toolbar,
            text="Create activity",
            command=self.create_activity,
            cursor="hand2",
        ).grid(row=0, column=2)

        self.canvas = tk.Canvas(content, bg="#F4F5F7", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            content,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.cards_frame = tk.Frame(self.canvas, bg="#F4F5F7")

        self.cards_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw",
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.cards_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.cards_window,
                width=event.width,
            ),
        )

        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

    def _load_activities(self):
        connection = None
        cursor = None

        try:
            connection = start_connection()
            cursor = connection.cursor()
            rows = get_activity_offerings(cursor)
            self.activities = [
                Offering.from_query_row(row) for row in rows
            ]
            self._show_activities(self.activities)

        except Exception as error:
            messagebox.showerror(
                "Activities",
                f"Could not load activities:\n{error}",
                parent=self,
            )

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    def _show_activities(self, activities):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not activities:
            tk.Label(
                self.cards_frame,
                text="No activities found.",
                bg="#F4F5F7",
                fg="#666666",
                font=("Arial", 11),
            ).pack(padx=16, pady=20)
            return

        for activity in activities:
            card = ActivitySlide(
                self.cards_frame,
                activity=activity,
                on_modify=self.modify_activity,
            )
            card.pack(fill="x", padx=16, pady=8)

    def _search_activities(self, _event=None):
        query = self.search_var.get().strip().casefold()

        matching_activities = [
            activity
            for activity in self.activities
            if query in (activity.name or "").casefold()
            or query in (activity.description or "").casefold()
            or query in (activity.activity_type or "").casefold()
            or query in (activity.instructor_name or "").casefold()
        ]

        self._show_activities(matching_activities)

    def create_activity(self):
        messagebox.showinfo(
            "Create activity",
            "Open the activity creation form here.",
            parent=self,
        )

    def modify_activity(self, activity):
        messagebox.showinfo(
            "Modify activity",
            f"Open the edit form for '{activity.name}' "
            f"(offering ID: {activity.offering_id}) here.",
            parent=self,
        )
