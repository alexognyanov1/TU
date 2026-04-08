-- =============================================
-- Задача 1: База данни за прожекции на филми
-- =============================================

DROP DATABASE IF EXISTS cinemas_db;
CREATE DATABASE cinemas_db;
USE cinemas_db;

CREATE TABLE cinemas_db.cinemas (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE cinemas_db.halls (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    cinema_id INT NOT NULL,
    number    INT NOT NULL,
    status    ENUM('Standard', 'VIP', 'Deluxe') NOT NULL DEFAULT 'Standard',
    CONSTRAINT FOREIGN KEY (cinema_id) REFERENCES cinemas(id),
    UNIQUE KEY (cinema_id, number)
);

CREATE TABLE cinemas_db.movies (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(255) NOT NULL,
    year    YEAR         NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE cinemas_db.screenings (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    hall_id       INT      NOT NULL,
    movie_id      INT      NOT NULL,
    screeningTime DATETIME NOT NULL,
    ticketsBought INT      NOT NULL DEFAULT 0,
    CONSTRAINT FOREIGN KEY (hall_id)  REFERENCES halls(id),
    CONSTRAINT FOREIGN KEY (movie_id) REFERENCES movies(id)
);

INSERT INTO cinemas VALUES
    (NULL, 'Arena Mladost'),
    (NULL, 'Cinema City'),
    (NULL, 'Lumiere');

INSERT INTO halls VALUES
    (NULL, 1, 1, 'VIP'),
    (NULL, 1, 2, 'Deluxe'),
    (NULL, 1, 3, 'Standard'),
    (NULL, 2, 1, 'VIP'),
    (NULL, 2, 2, 'Standard'),
    (NULL, 3, 1, 'Deluxe');

INSERT INTO movies VALUES
    (NULL, 'Final Destination 7', 2024, 'USA'),
    (NULL, 'Inception', 2010, 'USA'),
    (NULL, 'Parasite', 2019, 'South Korea');

INSERT INTO screenings VALUES
    (NULL, 1, 1, '2024-06-01 18:00:00', 45),
    (NULL, 1, 1, '2024-06-01 21:00:00', 60),
    (NULL, 2, 1, '2024-06-01 20:00:00', 80),
    (NULL, 3, 1, '2024-06-01 19:00:00', 30),
    (NULL, 4, 1, '2024-06-01 18:30:00', 55),
    (NULL, 5, 2, '2024-06-01 20:00:00', 40),
    (NULL, 6, 1, '2024-06-01 19:30:00', 70);

-- =============================================
-- Задача 2: Кина, зали и времена за "Final Destination 7"
--           само за VIP или Deluxe зали
-- =============================================

SELECT c.name AS CinemaName, h.number AS HallNumber, s.screeningTime
FROM screenings s
JOIN halls  h ON s.hall_id  = h.id
JOIN cinemas c ON h.cinema_id = c.id
JOIN movies  m ON s.movie_id  = m.id
WHERE m.name = 'Final Destination 7'
  AND h.status IN ('VIP', 'Deluxe')
ORDER BY c.name, h.number;

-- =============================================
-- Задача 3: Общ брой зрители на "Final Destination 7"
--           във VIP зала на "Arena Mladost"
-- =============================================

SELECT SUM(s.ticketsBought) AS TotalViewers
FROM screenings s
JOIN halls   h ON s.hall_id  = h.id
JOIN cinemas c ON h.cinema_id = c.id
JOIN movies  m ON s.movie_id  = m.id
WHERE m.name   = 'Final Destination 7'
  AND h.status = 'VIP'
  AND c.name   = 'Arena Mladost';

-- =============================================
-- Задача 4 (school_sport_clubs): Двойки ученици
--           в една и съща футболна група (без повторения)
-- =============================================

USE school_sport_clubs;

SELECT s1.name AS Student1, s2.name AS Student2, sg.id AS GroupId
FROM student_sport ss1
JOIN student_sport ss2 ON ss1.sportGroup_id = ss2.sportGroup_id AND ss1.student_id < ss2.student_id
JOIN students s1 ON ss1.student_id = s1.id
JOIN students s2 ON ss2.student_id = s2.id
JOIN sportGroups sg ON ss1.sportGroup_id = sg.id
WHERE sg.sport_id = (SELECT id FROM sports WHERE name = 'Football');

-- =============================================
-- Задача 5: Ученици с тренировки в 8:00 + VIEW
-- =============================================

CREATE OR REPLACE VIEW studentsAt8 AS
SELECT s.name AS StudentName, s.class, sg.location, c.name AS CoachName
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg    ON ss.sportGroup_id = sg.id
JOIN coaches c         ON sg.coach_id = c.id
WHERE sg.hourOfTraining = '08:00:00';

SELECT * FROM studentsAt8;

-- =============================================
-- Задача 6: Спорт и брой ученици
-- =============================================

SELECT sp.name AS Sport, COUNT(DISTINCT ss.student_id) AS StudentCount
FROM sports sp
JOIN sportGroups sg ON sp.id = sg.sport_id
JOIN student_sport ss ON sg.id = ss.sportGroup_id
GROUP BY sp.id, sp.name;
