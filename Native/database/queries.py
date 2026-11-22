# ============================================================================
# INSERT TEST DATA AND TRANSACTIONS
# ============================================================================

# ----------------------------------------------------------------------------
# Test 1: Create persons and accounts
# ----------------------------------------------------------------------------

# CONSTANT (used for all persons given that each need a person and account)
def insert_person(cursor, full_name, email, phone):
    cursor.execute(
        """
        INSERT INTO person (full_name, email, phone)
        VALUES (%s, %s, %s)
        """,
        (full_name, email, phone),
    )
    return cursor.lastrowid


def insert_account(cursor, person_id, password_hash, email_verified):
    cursor.execute(
        """
        INSERT INTO account (person_id, password_hash, email_verified)
        VALUES (%s, %s, %s)
        """,
        (person_id, password_hash, email_verified),
    )

# 1.1 Create a student.


def insert_student(cursor, person_id):
    cursor.execute(
        """
        INSERT INTO student (person_id)
        VALUES (%s)
        """,
        (person_id,),
    )


# 1.2 Create an admin.
def insert_administrator(cursor, person_id):
    cursor.execute(
        """
        INSERT INTO administrator (person_id)
        VALUES (%s)
        """,
        (person_id,),
    )


# 1.3 Create an instructor.
def insert_instructor(cursor, person_id, employee_number):
    cursor.execute(
        """
        INSERT INTO instructor (person_id, employee_number)
        VALUES (%s, %s)
        """,
        (person_id, employee_number),
    )


# ----------------------------------------------------------------------------
# Test 2: Complete the student's registration details
# ----------------------------------------------------------------------------
# This category contains an UPDATE, not an INSERT, so it isn't included here.


# ----------------------------------------------------------------------------
# Test 3: The admin approves accounts
# ----------------------------------------------------------------------------
# These account-approval statements are UPDATEs, not INSERTs.


# ----------------------------------------------------------------------------
# Test 4: Create Activities and Offerings
# ----------------------------------------------------------------------------

def insert_activity(cursor, name, description, activity_type, default_credits):
    cursor.execute(
        """
        INSERT INTO activity (name, description, activity_type, default_credits)
        VALUES (%s, %s, %s, %s)
        """,
        (name, description, activity_type, default_credits),
    )
    return cursor.lastrowid


def insert_offering(cursor, activity_id, instructor_id):
    cursor.execute(
        """
        INSERT INTO offering (activity_id, instructor_id)
        VALUES (%s, %s)
        """,
        (activity_id, instructor_id),
    )
    return cursor.lastrowid


# ----------------------------------------------------------------------------
# Test 5: Sessions
# ----------------------------------------------------------------------------

def insert_session(cursor, offering_id, session_date):
    cursor.execute(
        """
        INSERT INTO session (offering_id, session_date)
        VALUES (%s, %s)
        """,
        (offering_id, session_date),
    )
    return cursor.lastrowid


# ----------------------------------------------------------------------------
# Test 6: Inscription (Enrollment & Withdrawal)
# ----------------------------------------------------------------------------
# The withdrawal statement is an UPDATE, not an INSERT.

def insert_inscription(cursor, student_id, offering_id, status="enrolled"):
    cursor.execute(
        """
        INSERT INTO inscription (student_id, offering_id, status)
        VALUES (%s, %s, %s)
        """,
        (student_id, offering_id, status),
    )
    return cursor.lastrowid


# ----------------------------------------------------------------------------
# Test 7: Record Attendance
# ----------------------------------------------------------------------------

def insert_attendance(cursor, session_id, inscription_id, is_present):
    cursor.execute(
        """
        INSERT INTO attendance (session_id, inscription_id, is_present)
        VALUES (%s, %s, %s)
        """,
        (session_id, inscription_id, is_present),
    )
    return cursor.lastrowid


# ----------------------------------------------------------------------------
# Test 8: Working with Credits
# ----------------------------------------------------------------------------

def insert_credit(cursor, student_id, activity_id, credit_amount):
    cursor.execute(
        """
        INSERT INTO credit (student_id, activity_id, credit_amount)
        VALUES (%s, %s, %s)
        """,
        (student_id, activity_id, credit_amount),
    )
    return cursor.lastrowid



# ============================================================================
# DQL QUERIES / TESTS
# ============================================================================

# Test 1: Show all students along with their credits and show the activities
# in which they earned them
def get_student_credits_and_activities(cursor):
    cursor.execute(
        """
        SELECT
            s.student_number,
            p.full_name AS student_name,
            a.name AS activity_name,
            a.activity_type,
            c.credit_amount,
            c.earned_at
        FROM credit c
        JOIN student s ON c.student_id = s.person_id
        JOIN person p ON s.person_id = p.person_id
        JOIN activity a ON c.activity_id = a.activity_id
        """
    )
    return cursor.fetchall()


# Test 2: Showing user's data

# Test 2.1 Show all data from a student except for their credits
def get_student_details(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            p.phone,
            s.student_number,
            s.sex,
            s.entry_year,
            s.status,
            acc.email_verified,
            acc.status AS account_status
        FROM student s
        JOIN person p ON s.person_id = p.person_id
        LEFT JOIN account acc ON s.person_id = acc.person_id
        """
    )
    return cursor.fetchall()


# Test 2.2 Show all data from an instructor
def get_instructor_details(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            p.phone,
            i.employee_number,
            acc.email_verified,
            acc.status AS account_status
        FROM instructor i
        JOIN person p ON i.person_id = p.person_id
        LEFT JOIN account acc ON i.person_id = acc.person_id
        """
    )
    return cursor.fetchall()


# Test 2.3 Show all data from an admin
def get_administrator_details(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            p.phone,
            acc.email_verified,
            acc.status AS account_status
        FROM administrator adm
        JOIN person p ON adm.person_id = p.person_id
        LEFT JOIN account acc ON adm.person_id = acc.person_id
        """
    )
    return cursor.fetchall()


# Test 3: Show accounts pending approval accounts
def get_pending_accounts(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            acc.status AS account_status,
            acc.email_verified
        FROM account acc
        JOIN person p ON acc.person_id = p.person_id
        WHERE acc.status = %s
        """,
        ("pending",),
    )
    return cursor.fetchall()


# Test 3.1 Show accounts pending approval (administrators)
def get_pending_administrator_accounts(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            acc.status AS account_status
        FROM account acc
        JOIN administrator adm ON acc.person_id = adm.person_id
        JOIN person p ON acc.person_id = p.person_id
        WHERE acc.status = %s
        """,
        ("pending",),
    )
    return cursor.fetchall()


# Test 3.2 Show accounts pending approval (instructors)
def get_pending_instructor_accounts(cursor):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            i.employee_number,
            acc.status AS account_status
        FROM account acc
        JOIN instructor i ON acc.person_id = i.person_id
        JOIN person p ON acc.person_id = p.person_id
        WHERE acc.status = %s
        """,
        ("pending",),
    )
    return cursor.fetchall()


# Test 4: Show activities qwith their data
# Test 4.1: Show all available clubs and extracurriculars with their main data
def get_activity_offerings(cursor):
    cursor.execute(
        """
        SELECT
            o.offering_id,
            a.activity_id,
            a.name AS activity_name,
            a.description,
            a.activity_type,
            a.default_credits,
            o.max_students,
            p.full_name AS instructor_name,
            i.employee_number,
            (
                SELECT COUNT(*)
                FROM inscription ins
                WHERE ins.offering_id = o.offering_id
                  AND ins.status = %s
            ) AS student_count
        FROM offering o
        JOIN activity a ON o.activity_id = a.activity_id
        LEFT JOIN instructor i ON o.instructor_id = i.person_id
        LEFT JOIN person p ON i.person_id = p.person_id
        WHERE LOWER(a.activity_type) IN (%s, %s)
        """,
        ("enrolled", "club", "extracurricular"),
    )
    return cursor.fetchall()

# Test 4.2: Show all emergents
def get_emergent_offerings(cursor):
    cursor.execute(
        """
        SELECT
            o.offering_id,
            a.activity_id,
            a.name AS activity_name,
            a.description,
            a.activity_type,
            a.default_credits,
            o.max_students,
            p.full_name AS instructor_name,
            i.employee_number,
            (
                SELECT COUNT(*)
                FROM inscription ins
                WHERE ins.offering_id = o.offering_id
                  AND ins.status = %s
            ) AS student_count
        FROM offering o
        JOIN activity a ON o.activity_id = a.activity_id
        LEFT JOIN instructor i ON o.instructor_id = i.person_id
        LEFT JOIN person p ON i.person_id = p.person_id
        WHERE LOWER(a.activity_type) = %s
        """,
        ("enrolled", "emergent"),
    )
    return cursor.fetchall()



# Test 5: Show all students inside an activity

# Test 5.1 Show all students inside an extracurricular
# Test 5.2 Show all students inside a club
def get_enrolled_students_by_activity_type(cursor, activity_type):
    cursor.execute(
        """
        SELECT
            s.student_number,
            p.full_name AS student_name,
            a.name AS offering_activity_name,
            ins.status AS inscription_status,
            ins.inscribed_at
        FROM inscription ins
        JOIN offering o ON ins.offering_id = o.offering_id
        JOIN activity a ON o.activity_id = a.activity_id
        JOIN student s ON ins.student_id = s.person_id
        JOIN person p ON s.person_id = p.person_id
        WHERE a.activity_type = %s
          AND ins.status = %s
        """,
        (activity_type, "enrolled"),
    )
    return cursor.fetchall()


def get_enrolled_extracurricular_students(cursor):
    return get_enrolled_students_by_activity_type(cursor, "extracurricular")


def get_enrolled_club_students(cursor):
    return get_enrolled_students_by_activity_type(cursor, "club")


# Test 5.3 Show all students inside an emergent
def get_enrolled_students_in_emergent_activities(cursor):
    cursor.execute(
        """
        SELECT
            s.student_number,
            p.full_name AS student_name,
            a.name AS activity_name,
            ins.status AS inscription_status
        FROM inscription ins
        JOIN offering o ON ins.offering_id = o.offering_id
        JOIN activity a ON o.activity_id = a.activity_id
        JOIN student s ON ins.student_id = s.person_id
        JOIN person p ON s.person_id = p.person_id
        WHERE a.activity_type = %s
          AND ins.status = %s
        """,
        ("emergent", "enrolled"),
    )
    return cursor.fetchall()


# Test 6: Show the credits history and an operation of how many credits are
# missing according to the earned credits so far (Credits Target: 100 credits)
def get_student_credit_progress(cursor, credit_target=100):
    cursor.execute(
        """
        SELECT
            s.student_number,
            p.full_name AS student_name,
            COALESCE(SUM(c.credit_amount), 0) AS earned_credits_total,
            GREATEST(
                0,
                %s - COALESCE(SUM(c.credit_amount), 0)
            ) AS credits_remaining_to_target
        FROM student s
        JOIN person p ON s.person_id = p.person_id
        LEFT JOIN credit c ON s.person_id = c.student_id
        GROUP BY s.person_id, s.student_number, p.full_name
        """,
        (credit_target,),
    )
    return cursor.fetchall()


# Test 7: Show the attendance list for a specific extracurricular
# (not clubs nor emergents)
def get_extracurricular_attendance(cursor):
    cursor.execute(
        """
        SELECT
            s.student_number,
            p.full_name AS student_name,
            ses.session_date,
            att.is_present
        FROM attendance att
        JOIN session ses ON att.session_id = ses.session_id
        JOIN inscription ins ON att.inscription_id = ins.inscription_id
        JOIN student s ON ins.student_id = s.person_id
        JOIN person p ON s.person_id = p.person_id
        JOIN offering o ON ses.offering_id = o.offering_id
        JOIN activity a ON o.activity_id = a.activity_id
        WHERE a.activity_type = %s
        ORDER BY ses.session_date, p.full_name
        """,
        ("extracurricular",),
    )
    return cursor.fetchall()

def get_user_id(cursor):
    cursor.execute(
        """
        SELECT id FROM users WHERE email = %s
        """
    )
    return cursor.lastrowid

def get_administrator_by_email(cursor, email):
    cursor.execute(
        """
        SELECT
            p.person_id,
            p.full_name,
            p.email,
            p.phone,
            acc.password_hash,
            acc.email_verified,
            acc.status AS account_status
        FROM administrator adm
        JOIN person p ON adm.person_id = p.person_id
        JOIN account acc ON adm.person_id = acc.person_id
        WHERE p.email = %s
        """,
        (email,),
    )
    return cursor.fetchone()
