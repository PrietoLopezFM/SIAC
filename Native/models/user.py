from database.queries import get_administrator_details
from database.connection import start_connection

class Person:
    def __init__(self, full_name, email, email_verified, phone, db_id):
        self.full_name = full_name
        self.email = email
        self.email_verified = email_verified
        self.phone = phone
        self.db_id = db_id

    def show_field(self, field):
        """Print one field, such as show_field("email")."""
        if field not in ("full_name", "email", "email_verified", "phone", "db_id"):
            raise ValueError(f"Unknown Person field: {field}")

        print(getattr(self, field))


class Admin(Person):
    def __init__(
        self, full_name, email, phone, db_id,
        email_verified, account_status,
    ):
        super().__init__(full_name, email, email_verified, phone, db_id)
        self.email_verified = email_verified
        self.account_status = account_status


class Instructor(Person):
    pass


class Student(Person):
    def __init__(
        self, full_name, email, email_verified, phone, db_id,
        student_number, sex, entry_year, status,
        term="", current_club="", credits=0, club_history=None
    ):
        """
        The last four fields are optional so older code that builds a Student
        without them keeps working. They feed the Students and Reportes tables.

        term:         cuatrimestre the student is currently in.
        current_club: name of the club the student is in right now.
        credits:      accumulated credits (the tables show them as 'X/100').
        club_history: dict {period: club name}, e.g. {"Sep-Dic 2026": "Futbol"}.
        """
        super().__init__(full_name, email, email_verified, phone, db_id)
        self.student_number = student_number
        self.sex = sex
        self.entry_year = entry_year
        self.status = status
        self.term = term
        self.current_club = current_club
        self.credits = credits
        self.club_history = club_history if club_history is not None else {}

    def show_field(self, field):
        student_fields = (
            "student_number", "sex", "entry_year", "status",
            "term", "current_club", "credits", "club_history",
        )

        if field in student_fields:
            print(getattr(self, field))
        else:
            super().show_field(field)


class Activity:
    def __init__(self, name, description, activity_type, credits, quota):
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.credits = credits
        self.quota = quota

    def show_field(self, field):
        if field not in ("name", "description", "activity_type", "credits", "quota"):
            raise ValueError(f"Unknown Activity field: {field}")

        print(getattr(self, field))
