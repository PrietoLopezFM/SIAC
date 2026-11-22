class Offering:
    def __init__(
        self,
        offering_id,
        activity_id,
        name,
        description,
        activity_type,
        credits,
        max_students,
        instructor_name,
        employee_number,
        student_count=0,
    ):
        self.offering_id = offering_id
        self.activity_id = activity_id
        self.name = name
        self.description = description
        self.activity_type = activity_type
        self.credits = credits
        self.max_students = max_students
        self.instructor_name = instructor_name
        self.employee_number = employee_number
        self.student_count = student_count

    @classmethod
    def from_query_row(cls, row):
        return cls(
            offering_id=row[0],
            activity_id=row[1],
            name=row[2],
            description=row[3],
            activity_type=row[4],
            credits=row[5],
            max_students=row[6],
            instructor_name=row[7],
            employee_number=row[8],
            student_count=row[9],
        )
