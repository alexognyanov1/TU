CREATE DATABASE IF NOT EXISTS school_sport_clubs
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE school_sport_clubs;

CREATE TABLE sports (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE coaches (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE students (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    class VARCHAR(10)  NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE trainings (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    sport_id   INT          NOT NULL,
    coach_id   INT          NOT NULL,
    location   VARCHAR(100) NOT NULL,
    start_time TIME         NOT NULL,
    CONSTRAINT fk_training_sport FOREIGN KEY (sport_id) REFERENCES sports(id),
    CONSTRAINT fk_training_coach FOREIGN KEY (coach_id) REFERENCES coaches(id)
);

CREATE TABLE student_trainings (
    student_id  INT NOT NULL,
    training_id INT NOT NULL,
    PRIMARY KEY (student_id, training_id),
    CONSTRAINT fk_st_student  FOREIGN KEY (student_id)  REFERENCES students(id),
    CONSTRAINT fk_st_training FOREIGN KEY (training_id) REFERENCES trainings(id)
);

INSERT INTO sports (name) VALUES
    ('Football'),
    ('Volleyball'),
    ('Basketball');

INSERT INTO coaches (name) VALUES
    ('Peter Georgiev'),
    ('Maria Todorova'),
    ('Ivan Stoyanov');

INSERT INTO students (name, class, phone) VALUES
    ('Iliyan Ivanov',   '10A', '0888111222'),
    ('Georgi Petrov',   '10A', '0888333444'),
    ('Nikola Dimitrov', '11B', '0888555666'),
    ('Elena Kovacheva', '11B', '0888777888'),
    ('Teodora Hristova','12C', '0888999000');

INSERT INTO trainings (sport_id, coach_id, location, start_time) VALUES
    (1, 1, 'Stadium A',   '08:00:00'),
    (1, 1, 'Stadium B',   '10:00:00'),
    (2, 2, 'Sports Hall', '08:00:00'),
    (2, 3, 'Sports Hall', '14:00:00'),
    (3, 3, 'Gym 1',       '09:00:00');

INSERT INTO student_trainings (student_id, training_id) VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (1, 3),
    (4, 3),
    (5, 4),
    (3, 5);

-- Task 1
SELECT s.name, s.class, s.phone
FROM students s
JOIN student_trainings st ON s.id = st.student_id
JOIN trainings t ON st.training_id = t.id
JOIN sports sp ON t.sport_id = sp.id
WHERE sp.name = 'Football';

-- Task 2
SELECT DISTINCT c.name
FROM coaches c
JOIN trainings t ON c.id = t.coach_id
JOIN sports sp ON t.sport_id = sp.id
WHERE sp.name = 'Volleyball';

-- Task 3
SELECT c.name AS coach, sp.name AS sport
FROM coaches c
JOIN trainings t ON c.id = t.coach_id
JOIN sports sp ON t.sport_id = sp.id
JOIN student_trainings st ON t.id = st.training_id
JOIN students s ON st.student_id = s.id
WHERE s.name = 'Iliyan Ivanov';

-- Task 4
SELECT s.name AS student, s.class, t.location, c.name AS coach
FROM students s
JOIN student_trainings st ON s.id = st.student_id
JOIN trainings t ON st.training_id = t.id
JOIN coaches c ON t.coach_id = c.id
WHERE t.start_time = '08:00:00';
