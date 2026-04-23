USE school_sport_clubs;

# Task 1
DROP TRIGGER IF EXISTS salarypayments_after_delete;

DELIMITER $$
CREATE TRIGGER salarypayments_after_delete
AFTER DELETE ON salaryPayments
FOR EACH ROW
BEGIN
    INSERT INTO salarypayments_log (
        operation,
        old_coach_id,
        old_month,
        old_year,
        old_salaryAmount,
        old_dateOfPayment,
        dateOfLog
    ) VALUES (
        'DELETE',
        OLD.coach_id,
        OLD.month,
        OLD.year,
        OLD.salaryAmount,
        OLD.dateOfPayment,
        NOW()
    );
END$$
DELIMITER ;

# Task 2
DROP TRIGGER IF EXISTS student_sport_before_insert;

DELIMITER $$
CREATE TRIGGER student_sport_before_insert
BEFORE INSERT ON student_sport
FOR EACH ROW
BEGIN
    DECLARE group_count INT;

    SELECT COUNT(*) INTO group_count
    FROM student_sport
    WHERE student_id = NEW.student_id;

    IF group_count >= 2 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A student cannot be enrolled in more than 2 sport groups.';
    END IF;
END$$
DELIMITER ;

# Task 3
DROP VIEW IF EXISTS students_groups_count;

CREATE VIEW students_groups_count AS
SELECT
    s.name AS student_name,
    COUNT(ss.sportGroup_id) AS groups_count
FROM students s
LEFT JOIN student_sport ss ON ss.student_id = s.id
GROUP BY s.id, s.name;

# Task 4
DROP PROCEDURE IF EXISTS get_students_by_coach;

DELIMITER $$
CREATE PROCEDURE get_students_by_coach(IN coach_name VARCHAR(255))
BEGIN
    SELECT
        st.name AS student_name,
        sg.id AS group_id,
        sp.name AS sport_name
    FROM coaches c
    JOIN sportGroups sg ON sg.coach_id = c.id
    JOIN student_sport ss ON ss.sportGroup_id = sg.id
    JOIN students st ON st.id = ss.student_id
    JOIN sports sp ON sp.id = sg.sport_id
    WHERE c.name = coach_name;
END$$
DELIMITER ;

# Task 5
DROP PROCEDURE IF EXISTS get_groups_by_sport;

DELIMITER $$
CREATE PROCEDURE get_groups_by_sport(IN sport_name VARCHAR(255))
BEGIN
    SELECT
        c.name AS coach_name,
        sg.location,
        sg.hourOfTraining,
        sg.dayOfWeek
    FROM sports sp
    JOIN sportGroups sg ON sg.sport_id = sp.id
    JOIN coaches c ON c.id = sg.coach_id
    WHERE sp.name = sport_name;
END$$
DELIMITER ;
