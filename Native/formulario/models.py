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
        student_number, sex, entry_year, status
    ):
        super().__init__(full_name, email, inst_email, phone, db_id)
        self.student_number = student_number
        self.sex = sex
        self.entry_year = entry_year
        self.status = status

    def show_field(self, field):
        student_fields = ("student_number", "sex", "entry_year", "status")

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
    3, "S1001", "unspecified", 2025, "active"
)

test_user = User("Admin", "alex@utr.edu.mx", 1)


def authenticate_mock(email, password):
    """Return the mock user if the credentials match; otherwise return None."""
    if email == test_user.email and password == test_user.password:
        return test_user

    return None

test_activity = Activity(
    "Science Fair", "Annual student science fair", "academic", 3, 50
)
