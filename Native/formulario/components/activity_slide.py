import tkinter as tk

CARD_BG = "#FFFFFF"
TEXT = "#333333"
MUTED = "#666666"
ACCENT = "#B30000"


class ActivitySlide(tk.Frame):
    """A card displaying one offering and its activity details."""

    def __init__(self, parent, activity, on_modify=None):
        super().__init__(
            parent,
            bg=CARD_BG,
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            padx=16,
            pady=14,
        )
        self.activity = activity  # An Offering object
        self.on_modify = on_modify
        self._build_widgets()

    def _build_widgets(self):
        activity = self.activity

        tk.Label(
            self,
            text=activity.name or "",
            font=("Arial", 14, "bold"),
            bg=CARD_BG,
            fg=ACCENT,
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            self,
            text=activity.description or "",
            font=("Arial", 10),
            bg=CARD_BG,
            fg=TEXT,
            justify="left",
            wraplength=360,
            anchor="w",
        ).pack(fill="x", pady=(8, 12))

        quota = (
            str(activity.max_students)
            if activity.max_students is not None
            else "Not specified"
        )
        instructor = activity.instructor_name or "Not assigned"

        details = (
            ("Type", activity.activity_type or ""),
            ("Credits", activity.credits),
            ("Responsible", instructor),
            ("Students", f"{activity.student_count}/{quota} students"),
        )

        for label, value in details:
            tk.Label(
                self,
                text=f"{label}: {value}",
                font=("Arial", 9),
                bg=CARD_BG,
                fg=MUTED,
                anchor="w",
            ).pack(fill="x", pady=2)

        tk.Button(
            self,
            text="Modify",
            command=self._modify,
            cursor="hand2",
        ).pack(anchor="e", pady=(12, 0))

    def _modify(self):
        if self.on_modify:
            self.on_modify(self.activity)
