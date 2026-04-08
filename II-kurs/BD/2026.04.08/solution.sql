USE school_sport_clubs;

# Task 1
DROP PROCEDURE IF EXISTS sp_trainings_by_coach;
DELIMITER //
CREATE PROCEDURE sp_trainings_by_coach(IN p_coach_name VARCHAR(255))
BEGIN
    SELECT
        sp.name        AS sport_name,
        sg.location    AS location,
        sg.hourOfTraining AS training_hour,
        sg.dayOfWeek   AS training_day,
        st.name        AS student_name,
        st.phone       AS student_phone
    FROM coaches c
    JOIN sportGroups sg   ON sg.coach_id = c.id
    JOIN sports sp        ON sp.id = sg.sport_id
    JOIN student_sport ss ON ss.sportGroup_id = sg.id
    JOIN students st      ON st.id = ss.student_id
    WHERE c.name = p_coach_name
    ORDER BY sp.name, sg.dayOfWeek, sg.hourOfTraining, st.name;
END //
DELIMITER ;

# Task 2
DROP PROCEDURE IF EXISTS sp_sport_info_by_id;
DELIMITER //
CREATE PROCEDURE sp_sport_info_by_id(IN p_sport_id INT)
BEGIN
    SELECT
        sp.name AS sport_name,
        st.name AS student_name,
        c.name  AS coach_name
    FROM sports sp
    JOIN sportGroups sg   ON sg.sport_id = sp.id
    JOIN coaches c        ON c.id = sg.coach_id
    JOIN student_sport ss ON ss.sportGroup_id = sg.id
    JOIN students st      ON st.id = ss.student_id
    WHERE sp.id = p_sport_id
    ORDER BY st.name, c.name;
END //
DELIMITER ;

# Task 3
DROP PROCEDURE IF EXISTS sp_avg_taxes_by_student_year;
DELIMITER //
CREATE PROCEDURE sp_avg_taxes_by_student_year(
    IN p_student_name VARCHAR(255),
    IN p_year YEAR
)
BEGIN
    SELECT
        st.name AS student_name,
        p_year  AS year,
        AVG(tp.paymentAmount) AS average_payment
    FROM students st
    JOIN taxesPayments tp ON tp.student_id = st.id
    WHERE st.name = p_student_name
      AND tp.year = p_year
    GROUP BY st.id, st.name;
END //
DELIMITER ;

# Task 4
DROP PROCEDURE IF EXISTS sp_groups_count_by_coach;
DELIMITER //
CREATE PROCEDURE sp_groups_count_by_coach(IN p_coach_name VARCHAR(255))
BEGIN
    DECLARE v_count INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_count
    FROM coaches c
    JOIN sportGroups sg ON sg.coach_id = c.id
    WHERE c.name = p_coach_name;

    IF v_count = 0 THEN
        SELECT CONCAT('Coach "', p_coach_name, '" has no groups.') AS message;
    ELSE
        SELECT v_count AS groups_count;
    END IF;
END //
DELIMITER ;

# Task 5
DROP DATABASE IF EXISTS transaction_test;
CREATE DATABASE transaction_test;
USE transaction_test;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(255) NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0
);

INSERT INTO accounts (owner_name, balance) VALUES
    ('Ivan Petrov',   1000.00),
    ('Maria Ivanova',  500.00),
    ('Georgi Todorov', 250.00);

DROP PROCEDURE IF EXISTS sp_transfer_money;
DELIMITER //
CREATE PROCEDURE sp_transfer_money(
    IN p_from_id INT,
    IN p_to_id   INT,
    IN p_amount  DECIMAL(15,2)
)
BEGIN
    DECLARE v_balance DECIMAL(15,2) DEFAULT 0;
    DECLARE v_affected INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction failed due to a database error.' AS message;
    END;

    IF p_amount <= 0 THEN
        SELECT 'Transfer amount must be positive.' AS message;
    ELSE
        START TRANSACTION;

        SELECT balance INTO v_balance
        FROM accounts
        WHERE id = p_from_id
        FOR UPDATE;

        IF v_balance IS NULL THEN
            ROLLBACK;
            SELECT 'Source account not found.' AS message;
        ELSEIF v_balance < p_amount THEN
            ROLLBACK;
            SELECT 'Not enough money to perform the transaction.' AS message;
        ELSE
            UPDATE accounts
            SET balance = balance - p_amount
            WHERE id = p_from_id;

            IF ROW_COUNT() = 0 THEN
                ROLLBACK;
                SELECT 'Transaction failed: source account could not be debited.' AS message;
            ELSE
                UPDATE accounts
                SET balance = balance + p_amount
                WHERE id = p_to_id;

                SET v_affected = ROW_COUNT();
                IF v_affected = 0 THEN
                    ROLLBACK;
                    SELECT 'Transaction failed: destination account not found.' AS message;
                ELSE
                    COMMIT;
                    SELECT 'Transfer completed successfully.' AS message;
                END IF;
            END IF;
        END IF;
    END IF;
END //
DELIMITER ;
