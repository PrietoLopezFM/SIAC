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
  person_id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name            VARCHAR(150) NOT NULL,
  email                VARCHAR(150) NOT NULL,
  institutional_email  VARCHAR(150) NULL,
  phone                VARCHAR(20)  NULL,
  PRIMARY KEY (person_id),
  UNIQUE KEY uq_person_email (email),
  UNIQUE KEY uq_person_inst_email (institutional_email)
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
  email_verified   BOOLEAN NOT NULL DEFAULT FALSE,
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