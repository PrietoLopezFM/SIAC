-- ============================================================================
-- Oversimplified Club Management System Schema
-- ============================================================================
DROP DATABASE IF EXISTS siac_simple;

CREATE DATABASE IF NOT EXISTS siac_simple
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE siac_simple;

-- ----------------------------------------------------------------------------
-- 1. PEOPLE, ROLES AND ACCOUNTS
-- ----------------------------------------------------------------------------

CREATE TABLE person (
  person_id   INT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name   VARCHAR(150) NOT NULL,
  email       VARCHAR(150) NOT NULL,
  phone       VARCHAR(20) NULL,
  PRIMARY KEY (person_id),
  UNIQUE KEY uq_person_email (email)
) ENGINE=InnoDB;


CREATE TABLE administrator (
  person_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (person_id),
  CONSTRAINT fk_administrator_person
    FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE instructor (
  person_id        INT UNSIGNED NOT NULL,
  employee_number  VARCHAR(20) NULL,
  PRIMARY KEY (person_id),
  UNIQUE KEY uq_instructor_emp_num (employee_number),
  CONSTRAINT fk_instructor_person
    FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE student (
  person_id       INT UNSIGNED NOT NULL,
  student_number  VARCHAR(20) NULL,
  sex             VARCHAR(20) NULL,
  entry_year      SMALLINT UNSIGNED NOT NULL,
  status          ENUM('active','frozen','withdrawn') NOT NULL DEFAULT 'active',
  PRIMARY KEY (person_id),
  UNIQUE KEY uq_student_number (student_number),
  CONSTRAINT fk_student_person
    FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE account (
  person_id        INT UNSIGNED NOT NULL,
  password_hash    VARCHAR(255) NOT NULL,
  email_verified   ENUM('personal', 'institutional') NOT NULL DEFAULT 'personal',
  status           ENUM('pending','approved') NOT NULL DEFAULT 'pending',
  approved_by      INT UNSIGNED NULL,
  approved_at      DATETIME NULL,
  PRIMARY KEY (person_id),
  CONSTRAINT fk_account_person
    FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE,
  CONSTRAINT fk_account_approved_by
    FOREIGN KEY (approved_by) REFERENCES administrator (person_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 2. ACTIVITIES AND OFFERINGS
-- ----------------------------------------------------------------------------

CREATE TABLE activity (
  activity_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name           VARCHAR(120) NOT NULL,
  description    TEXT NULL,
  activity_type  ENUM('extracurricular', 'club', 'emergent') NOT NULL,
  default_credits TINYINT UNSIGNED NOT NULL DEFAULT 20,
  PRIMARY KEY (activity_id),
  UNIQUE KEY uq_activity_name (name)
) ENGINE=InnoDB;

CREATE TABLE offering (
  offering_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  activity_id    INT UNSIGNED NOT NULL,
  instructor_id  INT UNSIGNED NULL,
  PRIMARY KEY (offering_id),
  CONSTRAINT fk_offering_activity
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id) ON DELETE CASCADE,
  CONSTRAINT fk_offering_instructor
    FOREIGN KEY (instructor_id) REFERENCES instructor (person_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 3. INSCRIPTION / ENROLLMENT
-- ----------------------------------------------------------------------------

CREATE TABLE inscription (
  inscription_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  student_id      INT UNSIGNED NOT NULL,
  offering_id     INT UNSIGNED NOT NULL,
  inscribed_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status          ENUM('enrolled', 'withdrawn') NOT NULL DEFAULT 'enrolled',
  PRIMARY KEY (inscription_id),
  UNIQUE KEY uq_student_offering (student_id, offering_id),
  CONSTRAINT fk_inscription_student
    FOREIGN KEY (student_id) REFERENCES student (person_id) ON DELETE CASCADE,
  CONSTRAINT fk_inscription_offering
    FOREIGN KEY (offering_id) REFERENCES offering (offering_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 4. SESSIONS & ATTENDANCE
-- ----------------------------------------------------------------------------

CREATE TABLE session (
  session_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  offering_id   INT UNSIGNED NOT NULL,
  session_date  DATE NOT NULL,
  PRIMARY KEY (session_id),
  CONSTRAINT fk_session_offering
    FOREIGN KEY (offering_id) REFERENCES offering (offering_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE attendance (
  session_id      INT UNSIGNED NOT NULL,
  inscription_id  INT UNSIGNED NOT NULL,
  is_present      BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (session_id, inscription_id),
  CONSTRAINT fk_attendance_session
    FOREIGN KEY (session_id) REFERENCES session (session_id) ON DELETE CASCADE,
  CONSTRAINT fk_attendance_inscription
    FOREIGN KEY (inscription_id) REFERENCES inscription (inscription_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- 5. CREDITS
-- ----------------------------------------------------------------------------

CREATE TABLE credit (
  credit_id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
  student_id     INT UNSIGNED NOT NULL,
  activity_id    INT UNSIGNED NOT NULL,
  credit_amount  TINYINT UNSIGNED NOT NULL,
  earned_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (credit_id),
  CONSTRAINT fk_credit_student
    FOREIGN KEY (student_id) REFERENCES student (person_id) ON DELETE CASCADE,
  CONSTRAINT fk_credit_activity
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- ============================================================================
-- INSERT TEST DATA AND TRANSACTIONS
-- ============================================================================

START TRANSACTION;

-- ----------------------------------------------------------------------------
-- Test 1: Create persons and accounts
-- ----------------------------------------------------------------------------

-- 1.1 Create a student.
INSERT INTO person (full_name, email, phone)
VALUES ('Student1', 'st@personal.com', '1234');
SET @student_person_id = LAST_INSERT_ID();

INSERT INTO account (person_id, password_hash)
VALUES (@student_person_id, '1234');

INSERT INTO student (person_id, entry_year)
VALUES (@student_person_id, 2026);

-- 1.2 Create an admin
INSERT INTO person (full_name, email, phone)
VALUES ('Admin1', 'admin1@institution.com', '1111');
SET @admin_person_id = LAST_INSERT_ID();

INSERT INTO account (person_id, password_hash)
VALUES (@admin_person_id, '1234');

INSERT INTO administrator (person_id)
VALUES (@admin_person_id);

-- 1.3 Create an instructor
INSERT INTO person (full_name, email, phone)
VALUES ('Instructor1', 'instructor1@institution.com', '1111');
SET @instructor_person_id = LAST_INSERT_ID();

INSERT INTO account (person_id, password_hash)
VALUES (@instructor_person_id, '1234');

INSERT INTO instructor (person_id, employee_number)
VALUES (@instructor_person_id, 'EMP001');

-- ----------------------------------------------------------------------------
-- Test 2: Complete the student's registration details
-- ----------------------------------------------------------------------------
UPDATE student
SET student_number = '1234',
    sex = 'masculine',
    entry_year = 2026,
    status = 'active'
WHERE person_id = @student_person_id;

-- ----------------------------------------------------------------------------
-- Test 3: The admin approves accounts
-- ----------------------------------------------------------------------------

-- 3.1: Admin1's account approval
UPDATE account
SET status = 'approved',
    approved_by = @admin_person_id,
    approved_at = CURRENT_TIMESTAMP
WHERE person_id = @admin_person_id;

-- 3.2: Instructor1's account approval
UPDATE account
SET status = 'approved',
    approved_by = @admin_person_id,
    approved_at = CURRENT_TIMESTAMP
WHERE person_id = @instructor_person_id;

-- ----------------------------------------------------------------------------
-- Test 4: Create Activities and Offerings
-- ----------------------------------------------------------------------------

INSERT INTO activity (name, description, activity_type, default_credits)
VALUES ('Exxtracurriculars club', 'General club activities', 'club', 20);
SET @club_activity_id = LAST_INSERT_ID();

INSERT INTO activity (name, description, activity_type, default_credits)
VALUES ('Cooking', 'Cooking workshop and classes', 'extracurricular', 20);
SET @extra_activity_id = LAST_INSERT_ID();

INSERT INTO activity (name, description, activity_type, default_credits)
VALUES ('Lawnmowing Support', 'Community support emergent activity', 'emergent', 5);
SET @emergent_activity_id = LAST_INSERT_ID();

INSERT INTO offering (activity_id, instructor_id)
VALUES (@club_activity_id, @instructor_person_id);
SET @club_offering_id = LAST_INSERT_ID();

INSERT INTO offering (activity_id, instructor_id)
VALUES (@extra_activity_id, @instructor_person_id);
SET @extra_offering_id = LAST_INSERT_ID();

-- ----------------------------------------------------------------------------
-- Test 5: Sessions
-- ----------------------------------------------------------------------------

INSERT INTO session (offering_id, session_date)
VALUES (@extra_offering_id, '2026-08-24');
SET @extra_session_id = LAST_INSERT_ID();

-- ----------------------------------------------------------------------------
-- Test 6: Inscription (Enrollment & Withdrawal)
-- ----------------------------------------------------------------------------

-- 6.1: Enroll the student in the club
INSERT INTO inscription (student_id, offering_id, status)
VALUES (@student_person_id, @club_offering_id, 'enrolled');
SET @club_inscription_id = LAST_INSERT_ID();

-- 6.2: Withdraw the student from the club
UPDATE inscription
SET status = 'withdrawn'
WHERE inscription_id = @club_inscription_id;

-- 6.3: Enroll the student in the extracurricular activity
INSERT INTO inscription (student_id, offering_id, status)
VALUES (@student_person_id, @extra_offering_id, 'enrolled');
SET @extra_inscription_id = LAST_INSERT_ID();

-- ----------------------------------------------------------------------------
-- Test 7: Record Attendance
-- ----------------------------------------------------------------------------

INSERT INTO attendance (session_id, inscription_id, is_present)
VALUES (@extra_session_id, @extra_inscription_id, TRUE);

-- ----------------------------------------------------------------------------
-- Test 8: Working with Credits
-- ----------------------------------------------------------------------------

INSERT INTO credit (student_id, activity_id, credit_amount)
VALUES (@student_person_id, @emergent_activity_id, 5);

COMMIT;


-- ============================================================================
-- DQL QUERIES / TESTS
-- ============================================================================

-- Test 1: Show all students along with their credits and show the activities in which they earned them
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
JOIN activity a ON c.activity_id = a.activity_id;

-- Test 2: Showing user's data
-- Test 2.1 Show all data from a student except for their credits
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
LEFT JOIN account acc ON s.person_id = acc.person_id;

-- Test 2.2 Show all data from an instructor
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
LEFT JOIN account acc ON i.person_id = acc.person_id;

-- Test 2.3 Show all data from an admin
SELECT
    p.person_id,
    p.full_name,
    p.email,
    p.phone,
    acc.email_verified,
    acc.status AS account_status
FROM administrator adm
JOIN person p ON adm.person_id = p.person_id
LEFT JOIN account acc ON adm.person_id = acc.person_id;

-- Test 3: Show accounts pending approval accounts
SELECT
    p.person_id,
    p.full_name,
    p.email,
    acc.status AS account_status,
    acc.email_verified
FROM account acc
JOIN person p ON acc.person_id = p.person_id
WHERE acc.status = 'pending';

-- Test 3.1 Show accounts pending approval (administrators)
SELECT
    p.person_id,
    p.full_name,
    p.email,
    acc.status AS account_status
FROM account acc
JOIN administrator adm ON acc.person_id = adm.person_id
JOIN person p ON acc.person_id = p.person_id
WHERE acc.status = 'pending';

-- Test 3.2 Show accounts pending approval (instructors)
SELECT
    p.person_id,
    p.full_name,
    p.email,
    i.employee_number,
    acc.status AS account_status
FROM account acc
JOIN instructor i ON acc.person_id = i.person_id
JOIN person p ON acc.person_id = p.person_id
WHERE acc.status = 'pending';

-- Test 4: Show all available offers with their main data
SELECT
    o.offering_id,
    a.name AS activity_name,
    a.description,
    a.activity_type,
    a.default_credits,
    p.full_name AS instructor_name,
    i.employee_number
FROM offering o
JOIN activity a ON o.activity_id = a.activity_id
LEFT JOIN instructor i ON o.instructor_id = i.person_id
LEFT JOIN person p ON i.person_id = p.person_id;

-- Test 5: Show all students inside an activity
-- Test 5.1 Show all students inside an extracurricular
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
WHERE a.activity_type = 'extracurricular' AND ins.status = 'enrolled';

-- Test 5.2 Show all students inside a club
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
WHERE a.activity_type = 'club' AND ins.status = 'enrolled';

-- Test 5.3 Show all students inside an emergent
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
WHERE a.activity_type = 'emergent' AND ins.status = 'enrolled';

-- Test 6: Show the credits history and an operation of how many credits are missing according to the earned credits so far (Credits Target: 100 credits)
SELECT
    s.student_number,
    p.full_name AS student_name,
    COALESCE(SUM(c.credit_amount), 0) AS earned_credits_total,
    GREATEST(0, 100 - COALESCE(SUM(c.credit_amount), 0)) AS credits_remaining_to_100
FROM student s
JOIN person p ON s.person_id = p.person_id
LEFT JOIN credit c ON s.person_id = c.student_id
GROUP BY s.person_id, s.student_number, p.full_name;

-- Test 7: Show the attendance list for a specific extracurricular (not clubs nor emergents)
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
WHERE a.activity_type = 'extracurricular'
ORDER BY ses.session_date, p.full_name;

