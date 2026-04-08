# Task 1
USE school_sport_clubs;

CALL sp_trainings_by_coach('Ivan Todorov Petkov');
CALL sp_trainings_by_coach('georgi Ivanov Todorov');
CALL sp_trainings_by_coach('Slavi Petkov Petkov');

# Task 2
CALL sp_sport_info_by_id(1);
CALL sp_sport_info_by_id(2);
CALL sp_sport_info_by_id(4);

# Task 3
CALL sp_avg_taxes_by_student_year('Iliyan Ivanov', 2022);
CALL sp_avg_taxes_by_student_year('Ivan Iliev Georgiev', 2022);
CALL sp_avg_taxes_by_student_year('Iliyan Ivanov', 2020);
CALL sp_avg_taxes_by_student_year('Maria Hristova Dimova', 2022);

# Task 4
CALL sp_groups_count_by_coach('Ivan Todorov Petkov');
CALL sp_groups_count_by_coach('georgi Ivanov Todorov');
CALL sp_groups_count_by_coach('Slavi Petkov Petkov');
CALL sp_groups_count_by_coach('Nobody');

# Task 5
USE transaction_test;

SELECT * FROM accounts;

CALL sp_transfer_money(1, 2, 200.00);
SELECT * FROM accounts;

CALL sp_transfer_money(3, 1, 9999.00);

CALL sp_transfer_money(1, 2, 0);
CALL sp_transfer_money(1, 2, -50);

CALL sp_transfer_money(1, 999, 100.00);

CALL sp_transfer_money(999, 1, 100.00);

CALL sp_transfer_money(2, 3, 150.00);
SELECT * FROM accounts;
