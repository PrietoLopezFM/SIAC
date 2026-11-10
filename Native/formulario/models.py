class Person:
    def __init__(self, full_name, email, inst_email, phone, db_id):
        self.full_name = full_name
        self.email = email
        self.inst_email = inst_email
        self.phone = phone
        self.db_id = db_id

    def show_field(self, field):
        """Print one field, such as show_field("email")."""
        if field not in ("full_name", "email", "inst_email", "phone", "db_id"):
            raise ValueError(f"Unknown Person field: {field}")

        print(getattr(self, field))


class Admin(Person):
    pass


class Instructor(Person):
    pass


class Student(Person):
    def __init__(
        self, full_name, email, inst_email, phone, db_id,
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
        super().__init__(full_name, email, inst_email, phone, db_id)
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


class User:
    def __init__(self, password, email, db_id):
        self.password = password  # Kept for login testing, as requested
        self.email = email
        self.db_id = db_id

    def show_field(self, field):
        if field not in ("email", "db_id"):
            raise ValueError(f"Unknown User field: {field}")

        print(getattr(self, field))


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


# Test objects
test_admin = Admin(
    "Alex Admin", "alex@utr.edu.mx", False, "555-0100", 1
)

test_instructor = Instructor(
    "Morgan Lee", "morgan@utr.edu.mx", True, "555-0101", 2
)

test_student = Student(
    "Taylor Kim", "taylor@example.com", False, "555-0102",
    3, "S1001", "unspecified", 2025, "active",
    term=3,
    current_club="Futbol",
    credits=45,
    club_history={
        "Sep-Dic 2026": "Futbol",
        "Ene-Abr 2026": "Club de Lectura",
        "May-Ago 2026": "Ajedrez",
    },
)

# Extra students so the Students and Reportes tables show several rows.
test_student_2 = Student(
    "Sam Rivera", "sam@utr.edu.mx", True, "555-0103",
    4, "S1002", "unspecified", 2024, "active",
    term=6,
    current_club="Ajedrez",
    credits=80,
    club_history={
        "Sep-Dic 2026": "Ajedrez",
        "Ene-Abr 2026": "Futbol",
        "May-Ago 2026": "Club de Lectura",
    },
)

test_student_3 = Student(
    "Jordan Ortiz", "jordan@example.com", False, "555-0104",
    5, "S1003", "unspecified", 2026, "active",
    term=1,
    current_club="Club de Lectura",
    credits=10,
    club_history={
        "Sep-Dic 2026": "Club de Lectura",
    },
)

test_user = User("Admin", "alex@utr.edu.mx", 1)


# Mock "database" of people. It stands in for the person table until the
# real MySQL connection exists. When that happens, get_person_by_user()
# and get_students() should become queries instead of loops over this list.
MOCK_PEOPLE = [
    test_admin, test_instructor,
    test_student, test_student_2, test_student_3,
]


def authenticate_mock(email, password):
    """Return the mock user if the credentials match; otherwise return None."""
    if email == test_user.email and password == test_user.password:
        return test_user

    return None


def get_person_by_user(user):
    """Return the Person linked to this account (matching db_id), or None.

    An account (User) and a Person share the same db_id, so test_user
    (db_id 1) resolves to test_admin ("Alex Admin").
    """
    for person in MOCK_PEOPLE:
        if person.db_id == user.db_id:
            return person

    return None


def get_students():
    """Return only the Student objects (no admins nor instructors).

    Used by the Students and Reportes windows to build their tables.
    """
    return [person for person in MOCK_PEOPLE if isinstance(person, Student)]


test_activity = Activity(
    "Science Fair", "Annual student science fair", "academic", 3, 50
)