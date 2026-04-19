USE school_sport_clubs;

# Task 1
CREATE OR REPLACE VIEW coach_group_salary AS
SELECT
    c.name AS name,
    CONCAT(sg.id, ' - ', sg.location) AS groupInfo,
    s.name AS sportName,
    sp.year,
    sp.month,
    sp.salaryAmount
FROM coaches c
JOIN sportGroups sg ON sg.coach_id = c.id
JOIN sports s ON s.id = sg.sport_id
JOIN salaryPayments sp ON sp.coach_id = c.id
WHERE sp.month = MONTH(CURDATE())
  AND sp.year = YEAR(CURDATE());

SELECT * FROM coach_group_salary;

# Task 2
DROP PROCEDURE IF EXISTS students_in_multiple_groups;
DELIMITER //
CREATE PROCEDURE students_in_multiple_groups()
BEGIN
    SELECT st.name
    FROM students st
    JOIN student_sport ss ON ss.student_id = st.id
    GROUP BY st.id, st.name
    HAVING COUNT(ss.sportGroup_id) > 1;
END //
DELIMITER ;

CALL students_in_multiple_groups();

# Task 3
DROP PROCEDURE IF EXISTS coaches_without_groups;
DELIMITER //
CREATE PROCEDURE coaches_without_groups()
BEGIN
    SELECT c.name
    FROM coaches c
    LEFT JOIN sportGroups sg ON sg.coach_id = c.id
    WHERE sg.id IS NULL;
END //
DELIMITER ;

CALL coaches_without_groups();

# Task 4
DROP DATABASE IF EXISTS transaction_test;
CREATE DATABASE transaction_test;
USE transaction_test;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL DEFAULT 'BGN'
) ENGINE = InnoDB;

DROP PROCEDURE IF EXISTS convert_currency;
DELIMITER //
CREATE PROCEDURE convert_currency(
    IN p_amount DECIMAL(15,2),
    IN p_from_currency VARCHAR(3),
    IN p_to_currency VARCHAR(3),
    OUT p_result DECIMAL(15,2)
)
BEGIN
    DECLARE bnb_rate DECIMAL(10,5) DEFAULT 1.95583;

    IF p_from_currency = 'BGN' AND p_to_currency = 'EUR' THEN
        SET p_result = p_amount / bnb_rate;
    ELSEIF p_from_currency = 'EUR' AND p_to_currency = 'BGN' THEN
        SET p_result = p_amount * bnb_rate;
    ELSE
        SET p_result = p_amount;
    END IF;
END //
DELIMITER ;

# Task 5
DROP PROCEDURE IF EXISTS transfer_money;
DELIMITER //
CREATE PROCEDURE transfer_money(
    IN p_from_account INT,
    IN p_to_account INT,
    IN p_amount DECIMAL(15,2)
)
BEGIN
    DECLARE v_from_balance DECIMAL(15,2);
    DECLARE v_from_currency VARCHAR(3);
    DECLARE v_to_currency VARCHAR(3);
    DECLARE v_converted_amount DECIMAL(15,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Грешка: Трансакцията е неуспешна!' AS error_message;
    END;

    SELECT balance, currency INTO v_from_balance, v_from_currency
    FROM accounts WHERE id = p_from_account;

    SELECT currency INTO v_to_currency
    FROM accounts WHERE id = p_to_account;

    IF v_from_currency NOT IN ('BGN', 'EUR') OR v_to_currency NOT IN ('BGN', 'EUR') THEN
        SELECT 'Грешка: Валутата трябва да е BGN или EUR!' AS error_message;
    ELSEIF v_from_balance < p_amount THEN
        SELECT 'Грешка: Няма достатъчно средства по сметката!' AS error_message;
    ELSE
        IF v_from_currency != v_to_currency THEN
            CALL convert_currency(p_amount, v_from_currency, v_to_currency, v_converted_amount);
        ELSE
            SET v_converted_amount = p_amount;
        END IF;

        START TRANSACTION;
            UPDATE accounts SET balance = balance - p_amount WHERE id = p_from_account;
            UPDATE accounts SET balance = balance + v_converted_amount WHERE id = p_to_account;
        COMMIT;

        SELECT 'Трансакцията е успешна!' AS success_message;
    END IF;
END //
DELIMITER ;
