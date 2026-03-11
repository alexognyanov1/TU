USE school_sport_clubs;

-- 1
INSERT INTO students (name, egn, address, phone, class)
VALUES ('Ivan Ivanov Ivanov', '9207186371', 'Sofia-Serdika', '0888892950', '10');

-- 2
SELECT * FROM students
ORDER BY name ASC;

-- 3
DELETE FROM students
WHERE egn = '9207186371';

-- 4
SELECT s.name AS student_name, sp.name AS sport
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN sports sp ON sg.sport_id = sp.id;

-- 5
SELECT s.name AS student_name, s.class, sg.id AS group_id
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
WHERE sg.dayOfWeek = 'Monday';

-- 6
SELECT DISTINCT c.name AS coach_name
FROM coaches c
JOIN sportGroups sg ON c.id = sg.coach_id
JOIN sports sp ON sg.sport_id = sp.id
WHERE sp.name = 'Football';

-- 7
SELECT sg.location, sg.hourOfTraining, sg.dayOfWeek
FROM sportGroups sg
JOIN sports sp ON sg.sport_id = sp.id
WHERE sp.name = 'Volleyball';

-- 8
SELECT sp.name AS sport
FROM sports sp
JOIN sportGroups sg ON sp.id = sg.sport_id
JOIN student_sport ss ON sg.id = ss.sportGroup_id
JOIN students s ON ss.student_id = s.id
WHERE s.name = 'Iliyan Ivanov';

-- 9
SELECT s.name AS student_name
FROM students s
JOIN student_sport ss ON s.id = ss.student_id
JOIN sportGroups sg ON ss.sportGroup_id = sg.id
JOIN sports sp ON sg.sport_id = sp.id
JOIN coaches c ON sg.coach_id = c.id
WHERE sp.name = 'Football' AND c.name = 'Ivan Todorov Petkov';

-- 10
DROP DATABASE IF EXISTS car_service;
CREATE DATABASE car_service;
USE car_service;

CREATE TABLE car_service.clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    egn VARCHAR(10) NOT NULL UNIQUE,
    phone VARCHAR(20) NULL DEFAULT NULL,
    address VARCHAR(255) NULL DEFAULT NULL
);

CREATE TABLE car_service.cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate VARCHAR(20) NOT NULL UNIQUE,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year YEAR NOT NULL,
    client_id INT NOT NULL,
    CONSTRAINT FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE car_service.employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    egn VARCHAR(10) NOT NULL UNIQUE,
    position VARCHAR(100) NOT NULL
);

CREATE TABLE car_service.services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL DEFAULT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE car_service.repairs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    date DATE NOT NULL,
    description TEXT NULL DEFAULT NULL,
    CONSTRAINT FOREIGN KEY (car_id) REFERENCES cars(id)
);

CREATE TABLE car_service.repair_services (
    repair_id INT NOT NULL,
    service_id INT NOT NULL,
    PRIMARY KEY (repair_id, service_id),
    CONSTRAINT FOREIGN KEY (repair_id) REFERENCES repairs(id),
    CONSTRAINT FOREIGN KEY (service_id) REFERENCES services(id)
);

CREATE TABLE car_service.repair_employees (
    repair_id INT NOT NULL,
    employee_id INT NOT NULL,
    PRIMARY KEY (repair_id, employee_id),
    CONSTRAINT FOREIGN KEY (repair_id) REFERENCES repairs(id),
    CONSTRAINT FOREIGN KEY (employee_id) REFERENCES employees(id)
);

INSERT INTO clients (name, egn, phone, address) VALUES
('Georgi Petrov Ivanov',   '8503124561', '0888111222', 'Sofia, ul. Vitosha 12'),
('Maria Todorova Hristova','9112045678', '0877333444', 'Plovdiv, bul. Bulgaria 5'),
('Nikolay Georgiev Dimov', '7806231234', '0899555666', 'Varna, ul. Primorska 33'),
('Elena Stoyanova Koleva', '9405187890', '0888777888', 'Burgas, ul. Aleksandrovska 7');

INSERT INTO cars (plate, make, model, year, client_id) VALUES
('CB1234AB', 'Toyota',     'Corolla',  2018, 1),
('CB5678CD', 'BMW',        '320d',     2020, 1),
('CB9999EF', 'Volkswagen', 'Golf',     2015, 1),
('PB1111GH', 'Ford',       'Focus',    2019, 2),
('PB2222IJ', 'Opel',       'Astra',   2017, 2),
('B3333KL',  'Mercedes',   'C-Class',  2021, 3),
('B4444MN',  'Audi',       'A4',       2016, 3),
('H5555OP',  'Skoda',      'Octavia',  2022, 4);

SELECT
    c.id         AS client_id,
    c.name       AS client_name,
    c.egn        AS client_egn,
    c.phone      AS client_phone,
    c.address    AS client_address,
    ca.id        AS car_id,
    ca.plate     AS car_plate,
    ca.make      AS car_make,
    ca.model     AS car_model,
    ca.year      AS car_year
FROM clients c
JOIN cars ca ON ca.client_id = c.id
ORDER BY c.id, ca.id;