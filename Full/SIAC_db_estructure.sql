DROP DATABASE IF EXISTS SIAC;
CREATE DATABASE IF NOT EXISTS SIAC;
USE SIAC;

/*
COMPOSITE KEY - A key composed of two attributes, meaning that the combination of both attributes can only appear once.
    EX.
        The same terxm_id can appear in several rows with different milestone_type values, but the same pair cannot appear twice.
        If two separate primary keys were used instead, a student could only appear once in the whole table.

    Can two rows have the same value in this column but still be different records?
    Which combination of columns uniquely identifies each row?


CONSTRAINT - to prevent insertion of invalid data in a table, and ensures the accuracy and reliability of the data in the table. 
    If there is any violation between the constraint and the data action, the action is aborted.
        NOT NULL - Ensures that a column cannot have a NULL value
        UNIQUE - Ensures that all values in a column are unique
        PRIMARY KEY - Uniquely identifies each row in a table (a combination of a NOT NULL and UNIQUE)
        FOREIGN KEY - Establishes a link between data in two tables, and prevents action that will destroy the link between them
        CHECK - Ensures that the values in a column satisfies a specific condition
        DEFAULT - Sets a default value for a column if no value is specified
        CREATE INDEX - Creates indexes on columns to retrieve data from the database faster


UNSIGNED - An attribute which only allow positive numbers (no sign, duh)
*/

/*
General format
Name
    (Attributes, data type and behaviours)
    Attribute - constraints & primary, unique key

    primary & composite keys (I had a big problem earlier, so now they go together)
    
    unique keys

    foregin keys
*/


-- ----------------------------------------------------------------------------
-- 1. PEOPLE AND ROLES
-- ----------------------------------------------------------------------------

CREATE TABLE person (
  person_id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name            VARCHAR(150) NOT NULL,
  email                VARCHAR(150) NOT NULL,           -- login email
  institutional_email  VARCHAR(150) NULL ,               -- may be assigned weeks later
  phone                VARCHAR(20)  NULL,

  PRIMARY KEY (person_id),

  UNIQUE KEY (email),
  UNIQUE KEY (institutional_email)   -- several NULLs allowed
);

CREATE TABLE administrator (
  person_id INT UNSIGNED NOT NULL,

  PRIMARY KEY (person_id),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES person (person_id)
);

CREATE TABLE instructor (
  person_id        INT UNSIGNED NOT NULL,
  -- employee_number  VARCHAR(20) NULL UNIQUE KEY (employee_number) -- optional; a student instructor has none
  
  PRIMARY KEY (person_id),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES person (person_id)
);

CREATE TABLE student (
  person_id       INT UNSIGNED NOT NULL,
  student_number  VARCHAR(20) NULL,                     -- official ID (matrícula); NULL during the immersion term
  sex             VARCHAR(20) NULL,
  entry_year      SMALLINT UNSIGNED NOT NULL,           -- new students always enter in SEP-DEC
  status          ENUM('active','frozen','withdrawn') NOT NULL DEFAULT 'active',
  PRIMARY KEY (person_id),
  UNIQUE KEY (student_number),   -- unique and never reassigned
  
  CONSTRAINT fk_student_person FOREIGN KEY (person_id) REFERENCES person (person_id)
);

CREATE TABLE account (
  person_id        INT UNSIGNED NOT NULL,
  password_hash    VARCHAR(255) NOT NULL,               -- never the plain password
  email_verified   BOOLEAN NOT NULL DEFAULT FALSE,
  status           ENUM('pending','approved') NOT NULL DEFAULT 'pending',
  approved_by      INT UNSIGNED NULL,                   -- only applies to instructors
  approved_at      DATETIME NULL,

  PRIMARY KEY (person_id),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES person (person_id),
  CONSTRAINT FOREIGN KEY (approved_by) REFERENCES administrator (person_id)
);

-- ----------------------------------------------------------------------------
-- 2. ACADEMIC TERMS AND CALENDAR
-- ----------------------------------------------------------------------------

CREATE TABLE academic_term (
  term_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  term_year   YEAR NOT NULL,               -- year in which the term starts
  term_type   ENUM('SEP-DEC','JAN-APR','MAY-AUG') NOT NULL,
  start_date  DATE NOT NULL,                            -- start of week 1
  is_closed   BOOLEAN NOT NULL DEFAULT FALSE,

  PRIMARY KEY (term_id),

  UNIQUE KEY (term_year, term_type) -- Composed key :p
);

CREATE TABLE term_milestone (
  term_id         INT UNSIGNED NOT NULL,
  milestone_type  ENUM('offering_creation','enrollment','add_drop',
                       'preliminary_roster','official_roster',
                       'midterm_report','final_roster') NOT NULL,
   -- The various phases relevant for clubs. Creation, enrollment, join-leave, official roster, midterm report, final-roster.
   -- It may look weird to have a composite primary key, especially since milestone_type can change.
   -- This ensures that each term can have only one row for each milestone type.
  start_week TINYINT UNSIGNED NOT NULL, -- These values will always oscillate between 1 and no more than 21
  end_week TINYINT UNSIGNED NOT NULL,

  PRIMARY KEY (term_id, milestone_type), -- Another composite key :p

  CONSTRAINT CHECK (end_week >= start_week), -- The end week can't be less than the start week, duh
  CONSTRAINT FOREIGN KEY (term_id) REFERENCES academic_term (term_id)
);

CREATE TABLE student_term (
  person_id       INT UNSIGNED NOT NULL, -- No, person and term can't be primary keys each
  term_id         INT UNSIGNED NOT NULL, -- I mean, they have to be composed
  -- Similar case. Each student can only be in a single term once (each term is uniquely identified by the id)
  degree_program  VARCHAR(20) NOT NULL,                 -- degree program code //TDSM TSC... 
  group_letter    VARCHAR(5) NULL,                      -- A,B...
  term_number     TINYINT UNSIGNED NOT NULL,            -- 0 = immersion, 1... 4?
  
  PRIMARY KEY (person_id, term_id),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES student (person_id),
  CONSTRAINT FOREIGN KEY (term_id) REFERENCES academic_term (term_id)
);

-- ----------------------------------------------------------------------------
-- 3. ACTIVITIES AND OFFERINGS (one base table and one table per type)
-- ----------------------------------------------------------------------------

CREATE TABLE activity (
  activity_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name         VARCHAR(120) NOT NULL,

  PRIMARY KEY (activity_id),

  UNIQUE KEY (name)
);

CREATE TABLE offering (
  offering_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  activity_id    INT UNSIGNED NOT NULL,
  term_id        INT UNSIGNED NOT NULL,
  offering_type  ENUM('extracurricular','club','emergent') NOT NULL,

  PRIMARY KEY (offering_id),

  UNIQUE KEY (activity_id, term_id),         -- ties each activity to the term
  UNIQUE KEY (offering_id, offering_type),   -- ties each subtype table to its type
  UNIQUE KEY (offering_id, term_id),         -- ties enrollments and credits to the term

  CONSTRAINT FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
  CONSTRAINT FOREIGN KEY (term_id) REFERENCES academic_term (term_id)
);

CREATE TABLE extracurricular_offering (
  offering_id             INT UNSIGNED NOT NULL,
  offering_type           ENUM('extracurricular','club','emergent') NOT NULL DEFAULT 'extracurricular',
  capacity                SMALLINT UNSIGNED NOT NULL,
  weekly_hour_allocation  DECIMAL(4,1) NOT NULL,        -- hours assigned by the administrator
  instructor_id           INT UNSIGNED NOT NULL,
  location                VARCHAR(80) NULL,             -- fixed venue for the activity
  start_week              TINYINT UNSIGNED NOT NULL,    -- first week with classes
  end_week                TINYINT UNSIGNED NOT NULL,    -- last week with classes

  PRIMARY KEY (offering_id),

  CONSTRAINT CHECK (offering_type = 'extracurricular'),
  CONSTRAINT CHECK (capacity > 0),
  CONSTRAINT CHECK (weekly_hour_allocation > 0),
  CONSTRAINT CHECK (end_week >= start_week),


  CONSTRAINT FOREIGN KEY (offering_id, offering_type) REFERENCES offering (offering_id, offering_type), -- matches id and type
  CONSTRAINT FOREIGN KEY (instructor_id) REFERENCES instructor (person_id)
);

CREATE TABLE club_offering (
  offering_id     INT UNSIGNED NOT NULL,
  offering_type   ENUM('extracurricular','club','emergent') NOT NULL DEFAULT 'club',
  responsible_id  INT UNSIGNED NOT NULL,                -- club lead (most certain an instructor)

  PRIMARY KEY (offering_id),

  CONSTRAINT CHECK (offering_type = 'club'),

  CONSTRAINT FOREIGN KEY (offering_id, offering_type) REFERENCES offering (offering_id, offering_type),
  CONSTRAINT FOREIGN KEY (responsible_id) REFERENCES instructor (person_id)
);

CREATE TABLE emergent_offering (
  offering_id     INT UNSIGNED NOT NULL,
  offering_type   ENUM('extracurricular','club','emergent') NOT NULL DEFAULT 'emergent',
  description     TEXT NOT NULL,
  credit_amount   TINYINT UNSIGNED NOT NULL,            -- 5 to 20
  published_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  valid_until     DATE NULL,
  published_by    INT UNSIGNED NOT NULL,                -- administrator who posts the notice

  PRIMARY KEY (offering_id),

  CONSTRAINT CHECK (offering_type = 'emergent'),
  CONSTRAINT CHECK (credit_amount BETWEEN 5 AND 20),

  CONSTRAINT FOREIGN KEY (offering_id, offering_type) REFERENCES offering (offering_id, offering_type),
  CONSTRAINT FOREIGN KEY (published_by) REFERENCES administrator (person_id)
);

-- ----------------------------------------------------------------------------
-- 4. SCHEDULES: TIME BLOCKS, GROUPS AND SESSIONS (extracurricular only)
-- ----------------------------------------------------------------------------

CREATE TABLE time_block (
  block_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
  offering_id  INT UNSIGNED NOT NULL,
  day_of_week  ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') NOT NULL,
  start_time   TIME NOT NULL,
  end_time     TIME NOT NULL,

  PRIMARY KEY (block_id),

  UNIQUE KEY (block_id, offering_id),
  UNIQUE KEY (offering_id, day_of_week, start_time),

  CONSTRAINT CHECK (end_time > start_time),
  CONSTRAINT FOREIGN KEY (offering_id) REFERENCES extracurricular_offering (offering_id)
);

CREATE TABLE class_group (
  class_group_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  offering_id     INT UNSIGNED NOT NULL,
  name            VARCHAR(40) NOT NULL,

  PRIMARY KEY (class_group_id),

  UNIQUE KEY (class_group_id, offering_id),
  UNIQUE KEY (offering_id, name),

  CONSTRAINT FOREIGN KEY (offering_id) REFERENCES extracurricular_offering (offering_id)
);

-- Which blocks each group attends. The composite keys guarantee that the groups and the block belong to the same offering.
-- Editor's note: I'm gonna OFF myself.
CREATE TABLE class_group_block (
  class_group_id  INT UNSIGNED NOT NULL,
  block_id        INT UNSIGNED NOT NULL,
  offering_id     INT UNSIGNED NOT NULL,

  PRIMARY KEY (class_group_id, block_id),
  
  CONSTRAINT FOREIGN KEY (class_group_id, offering_id) REFERENCES class_group (class_group_id, offering_id),
  CONSTRAINT FOREIGN KEY (block_id, offering_id) REFERENCES time_block (block_id, offering_id)
);

-- One block in one specific week. The application generates them when the
-- offering is created.
CREATE TABLE session (
  session_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  block_id      INT UNSIGNED NOT NULL,
  week_number   TINYINT UNSIGNED NOT NULL,
  session_date  DATE NOT NULL,                          -- term start_date + week + weekday; may be adjusted
  status        ENUM('scheduled','closed','cancelled') NOT NULL DEFAULT 'scheduled',
  closed_by     INT UNSIGNED NULL,
  closed_at     DATETIME NULL,

  PRIMARY KEY (session_id),

  UNIQUE KEY (block_id, week_number),

  KEY (session_date), -- This bad boy here helps the database find sessions for a given date faster, instead of scanning every session row. :)

  CONSTRAINT FOREIGN KEY (block_id) REFERENCES time_block (block_id),
  CONSTRAINT FOREIGN KEY (closed_by) REFERENCES person (person_id)
);

-- ----------------------------------------------------------------------------
-- 5. ENROLLMENT AND ATTENDANCE
-- ----------------------------------------------------------------------------
-- Editor's note: I'm gonna cry :c
CREATE TABLE enrollment (
  enrollment_id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
  person_id                INT UNSIGNED NOT NULL,
  offering_id              INT UNSIGNED NOT NULL,
  term_id                  INT UNSIGNED NOT NULL,       -- copy of the offering's term (the composite key validates it)
  enrolled_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- set by the server

  status                   ENUM('enrolled','withdrawn') NOT NULL DEFAULT 'enrolled',
  source                   ENUM('form','administrator','club_list') NOT NULL DEFAULT 'form',

  class_group_id           INT UNSIGNED NULL,           -- empty until the instructor assigns it
  final_activity_completed BOOLEAN NULL,                -- NULL = not recorded yet
  dropped_at               DATETIME NULL,
  -- Generated column: 1 only while the enrollment is active.
  is_active                TINYINT GENERATED ALWAYS AS (CASE WHEN status = 'enrolled' THEN 1 ELSE NULL END) STORED,
    /*This one's a tricky one.
        It's there to make the database enforce “at most one active enrollment per student per term” 
        while still allowing withdrawn enrollments to remain as history.

            The UNIQUE KEY (person_id, term_id, is_active) uses that computed value:
                An active enrollment gets is_active = 1, 
                so a second active row with the same student and term would repeat the same key and be rejected.

                A withdrawn enrollment gets is_active = NULL, 
                so multiple withdrawn rows can be retained.
    */

  PRIMARY KEY (enrollment_id),

  -- One active enrollment per student and term (withdrawn rows remain as history).
  UNIQUE KEY (person_id, term_id, is_active), 
  UNIQUE KEY (enrollment_id, offering_id),

  KEY (offering_id, status), -- Another index, yayn't

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES student (person_id),
  CONSTRAINT FOREIGN KEY (offering_id, term_id) REFERENCES offering (offering_id, term_id),
  CONSTRAINT FOREIGN KEY (class_group_id, offering_id) REFERENCES class_group (class_group_id, offering_id)
);

CREATE TABLE attendance (
  session_id     INT UNSIGNED NOT NULL,
  enrollment_id  INT UNSIGNED NOT NULL,
  is_present     TINYINT UNSIGNED NOT NULL,             -- 1 present, 0 absent
  logged_by      INT UNSIGNED NULL,
  logged_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (session_id, enrollment_id),

  CONSTRAINT ck_attendance_is_present CHECK (is_present IN (0, 1)),

  CONSTRAINT FOREIGN KEY (session_id) REFERENCES session (session_id),
  CONSTRAINT FOREIGN KEY (enrollment_id) REFERENCES enrollment (enrollment_id),
  CONSTRAINT FOREIGN KEY (logged_by) REFERENCES person (person_id)
);

-- ----------------------------------------------------------------------------
-- 6. CREDITS
-- ----------------------------------------------------------------------------

CREATE TABLE assigned_credit (
  credit_id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
  person_id      INT UNSIGNED NOT NULL,
  term_id        INT UNSIGNED NOT NULL,
  offering_id    INT UNSIGNED NULL,                     -- NULL for historical credits from the old Excel file
  credit_reason  ENUM('participant','instructor','extra') NOT NULL,
  description    VARCHAR(255) NULL,
  credit_amount  TINYINT UNSIGNED NOT NULL,             -- 20 for extracurriculars and clubs, 5 to 20 for extras
  status         ENUM('pending','confirmed') NOT NULL DEFAULT 'pending',
  confirmed_by   INT UNSIGNED NULL,
  confirmed_at   DATETIME NULL,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (credit_id),
  -- The same credit is not granted twice for the same offering and reason.

  UNIQUE KEY (person_id, offering_id, credit_reason),

  KEY (person_id, term_id),

  CONSTRAINT CHECK (credit_amount BETWEEN 5 AND 20),
  CONSTRAINT CHECK (status = 'pending' OR confirmed_by IS NOT NULL),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES student (person_id),
  CONSTRAINT FOREIGN KEY (term_id) REFERENCES academic_term (term_id),
  CONSTRAINT FOREIGN KEY (offering_id, term_id) REFERENCES offering (offering_id, term_id),
  CONSTRAINT FOREIGN KEY (confirmed_by) REFERENCES administrator (person_id)
);

-- ----------------------------------------------------------------------------
-- 7. AUDIT
-- ----------------------------------------------------------------------------

-- Log of changes. person_id points to person (not administrator) so that an
-- action by any role, including an unauthorized one, can be recorded.
CREATE TABLE audit_log (
  audit_id      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  person_id     INT UNSIGNED NOT NULL,                  -- who performed the action
  action        VARCHAR(40) NOT NULL,                   -- e.g. 'confirm_credit', 'change_activity'
  target_table  VARCHAR(40) NOT NULL,                   -- table of the affected record
  record_id     VARCHAR(40) NOT NULL,                   -- key of the affected record
  description   VARCHAR(255) NULL,                      -- optional detail, e.g. 'status: pending -> confirmed'
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (audit_id),

  KEY (target_table, record_id),
  KEY (created_at),

  CONSTRAINT FOREIGN KEY (person_id) REFERENCES person (person_id)
);