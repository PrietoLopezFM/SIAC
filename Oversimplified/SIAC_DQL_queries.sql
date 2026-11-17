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