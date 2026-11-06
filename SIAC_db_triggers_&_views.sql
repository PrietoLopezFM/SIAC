USE SIAC;
-- ----------------------------------------------------------------------------
-- 8. TRIGGERS (rules that cross tables)
-- ----------------------------------------------------------------------------

DELIMITER $$

-- Nobody enrolls in an emergent offering: those only grant credits.
CREATE TRIGGER trg_enrollment_no_emergent
BEFORE INSERT ON enrollment
FOR EACH ROW
BEGIN
  IF (SELECT offering_type FROM offering WHERE offering_id = NEW.offering_id) = 'emergent' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Emergent offerings do not accept enrollments';
  END IF;
END$$

-- Attendance must belong to a session of the same offering as the enrollment.
CREATE TRIGGER trg_attendance_same_offering
BEFORE INSERT ON attendance
FOR EACH ROW
BEGIN
  IF (SELECT b.offering_id
        FROM session s
        JOIN time_block b ON b.block_id = s.block_id
       WHERE s.session_id = NEW.session_id)
     <> (SELECT e.offering_id
           FROM enrollment e
          WHERE e.enrollment_id = NEW.enrollment_id) THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'The enrollment and the session belong to different offerings';
  END IF;
END$$

DELIMITER ;



-- ----------------------------------------------------------------------------
-- 9. VIEWS (calculated values that are not stored)
-- ----------------------------------------------------------------------------

-- Attendance percentage to date, counting only closed sessions.
CREATE VIEW v_attendance_percentage AS
SELECT e.enrollment_id,
       e.person_id,
       e.offering_id,
       COUNT(s.session_id)                         AS recorded_session_count,
       COALESCE(SUM(a.is_present), 0)              AS attended_session_count,
       ROUND(100 * COALESCE(SUM(a.is_present), 0) / NULLIF(COUNT(s.session_id), 0), 1) AS attendance_percentage
  FROM enrollment e
  LEFT JOIN (attendance a
             JOIN session s ON s.session_id = a.session_id AND s.status = 'closed')
         ON a.enrollment_id = e.enrollment_id
 WHERE e.status = 'enrolled'
 GROUP BY e.enrollment_id, e.person_id, e.offering_id;

-- Official credits (confirmed), pending credits and distance to 100.
CREATE VIEW v_student_credit_summary AS
SELECT st.person_id,
       COALESCE(SUM(CASE WHEN ac.status = 'confirmed' THEN ac.credit_amount END), 0) AS official_credit_total,
       COALESCE(SUM(CASE WHEN ac.status = 'pending'   THEN ac.credit_amount END), 0) AS pending_credit_total,
       GREATEST(0, 100 - COALESCE(SUM(CASE WHEN ac.status = 'confirmed' THEN ac.credit_amount END), 0)) AS credit_remaining_to_100
  FROM student st
  LEFT JOIN assigned_credit ac ON ac.person_id = st.person_id
 GROUP BY st.person_id;

-- Seats taken per extracurricular offering (used to hide a full option in the sign-up form).
CREATE VIEW v_extracurricular_capacity AS
SELECT eo.offering_id,
       eo.capacity,
       COUNT(e.enrollment_id)                  AS enrolled_count,
       eo.capacity - COUNT(e.enrollment_id)    AS seats_available
  FROM extracurricular_offering eo
  LEFT JOIN enrollment e ON e.offering_id = eo.offering_id AND e.status = 'enrolled'
 GROUP BY eo.offering_id, eo.capacity;