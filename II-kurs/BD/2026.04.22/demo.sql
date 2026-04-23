USE school_sport_clubs;

# Task 1 - demo: trigger logs deleted salarypayments rows
SELECT * FROM salarypayments_log;

DELETE FROM salaryPayments
WHERE coach_id = 6 AND year = 2024;

SELECT * FROM salarypayments_log;

# Task 2 - demo: trigger blocks a 3rd group enrollment
SELECT * FROM student_sport WHERE student_id = 1;

# Valid - student 4 has only 1 group, adding a 2nd should succeed
INSERT INTO student_sport VALUES (4, 4);
SELECT * FROM student_sport WHERE student_id = 4;

# Invalid - student 1 already has 2 groups, trying to add a 3rd must fail
INSERT INTO student_sport VALUES (1, 4);

# Task 3 - demo: view shows full student name and group count
SELECT * FROM students_groups_count;

# Task 4 - demo: list students trained by a given coach
CALL get_students_by_coach('Ivan Todorov Petkov');

CALL get_students_by_coach('georgi Ivanov Todorov');

# Task 5 - demo: list coach name, location, hour and day for a given sport
CALL get_groups_by_sport('Football');

CALL get_groups_by_sport('Volleyball');
