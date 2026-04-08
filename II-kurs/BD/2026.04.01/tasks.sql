USE school_sport_clubs;

-- Task 1
SELECT s.name, s.class, s.phone
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN sports sp ON sg.sport_id = sp.id
WHERE sp.name = 'Football';

-- Task 2
SELECT DISTINCT c.name
FROM coaches c
JOIN sportGroups sg ON c.id = sg.coach_id
JOIN sports sp ON sg.sport_id = sp.id
WHERE sp.name = 'Volleyball';

-- Task 3
SELECT c.name AS coach, sp.name AS sport, sg.dayOfWeek, sg.location
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN sports sp ON sg.sport_id = sp.id
JOIN coaches c ON sg.coach_id = c.id
WHERE s.name = 'Maria Hristova Dimova';

-- Task 4
SELECT s.name AS student, tp.month, SUM(tp.paymentAmount) AS total_paid
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN coaches c ON sg.coach_id = c.id
JOIN taxesPayments tp ON tp.student_id = s.id AND tp.group_id = sg.id
WHERE c.egn = '7509041245'
GROUP BY s.id, tp.month
HAVING SUM(tp.paymentAmount) > 700
ORDER BY s.name, tp.month;

-- Task 5
SELECT COUNT(DISTINCT ss.student_id) AS football_students
FROM student_sport ss
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN sports sp ON sg.sport_id = sp.id
WHERE sp.name = 'Football';

-- Task 6
SELECT c.name AS coach, sp.name AS sport
FROM coaches c
LEFT JOIN sportGroups sg ON c.id = sg.coach_id
LEFT JOIN sports sp ON sg.sport_id = sp.id;

-- Task 7
SELECT sp.name AS sport, sg.location, COUNT(ss.student_id) AS student_count
FROM sportGroups sg
JOIN sports sp ON sg.sport_id = sp.id
JOIN student_sport ss ON sg.id = ss.sportGroup_id
GROUP BY sg.id, sp.name, sg.location
HAVING COUNT(ss.student_id) > 3;

-- Task 8
USE transaction_test;

START TRANSACTION;

UPDATE customer_accounts
SET amount = amount - 50000
WHERE customer_id = (SELECT id FROM customers WHERE name = 'Stoyan Pavlov Pavlov')
  AND currency = 'BGN';

UPDATE customer_accounts
SET amount = amount + 50000
WHERE customer_id = (SELECT id FROM customers WHERE name = 'Ivan Petrov Iordanov')
  AND currency = 'BGN';

COMMIT;
