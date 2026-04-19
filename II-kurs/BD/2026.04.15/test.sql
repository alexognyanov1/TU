# Test data for Task 1 - insert salary payments for current month
USE school_sport_clubs;

INSERT IGNORE INTO salaryPayments (coach_id, month, year, salaryAmount, dateOfPayment)
VALUES
    (1, MONTH(CURDATE()), YEAR(CURDATE()), 1200, NOW()),
    (2, MONTH(CURDATE()), YEAR(CURDATE()), 1300, NOW());

# Test Task 1 - VIEW
SELECT * FROM coach_group_salary;

# Test Task 2 - students in multiple groups
CALL students_in_multiple_groups();

# Test Task 3 - coaches without groups
CALL coaches_without_groups();

# Test data for Tasks 4 and 5
USE transaction_test;

INSERT INTO accounts (owner, balance, currency)
VALUES
    ('Ivan Petkov', 5000.00, 'BGN'),
    ('Georgi Todorov', 2000.00, 'EUR'),
    ('Petar Yordanov', 3000.00, 'USD');

# Test Task 4 - currency conversion
CALL convert_currency(1000, 'BGN', 'EUR', @result);
SELECT @result AS 'BGN 1000 -> EUR';

CALL convert_currency(500, 'EUR', 'BGN', @result);
SELECT @result AS 'EUR 500 -> BGN';

# Test Task 5 - transfer money

# Test: successful transfer (same currency)
SELECT 'Before transfer (same currency):' AS '';
SELECT id, owner, balance, currency FROM accounts WHERE id IN (1, 2);

# This transfers BGN->EUR, so convert_currency is called
CALL transfer_money(1, 2, 500.00);

SELECT 'After transfer BGN->EUR (500 BGN from account 1 to account 2):' AS '';
SELECT id, owner, balance, currency FROM accounts WHERE id IN (1, 2);

# Test: insufficient funds
CALL transfer_money(1, 2, 999999.00);

# Test: unsupported currency (account 3 is USD)
CALL transfer_money(1, 3, 100.00);
