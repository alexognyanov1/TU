-- Task 5
CREATE DATABASE IF NOT EXISTS hospital
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hospital;

CREATE TABLE specializations (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE doctors (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    first_name          VARCHAR(50)  NOT NULL,
    middle_name         VARCHAR(50)  NOT NULL,
    last_name           VARCHAR(50)  NOT NULL,
    office              VARCHAR(20)  NOT NULL,
    specialization_id   INT          NOT NULL,
    accepts_insurance   TINYINT(1)   NOT NULL DEFAULT 0,
    phone               VARCHAR(20),
    email               VARCHAR(100),
    CONSTRAINT fk_doctor_specialization FOREIGN KEY (specialization_id)
        REFERENCES specializations(id)
);

CREATE TABLE patients (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50)  NOT NULL,
    middle_name   VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    address       VARCHAR(200) NOT NULL,
    egn           CHAR(10)     NOT NULL UNIQUE,
    date_of_birth DATE,
    phone         VARCHAR(20),
    email         VARCHAR(100)
);

CREATE TABLE medications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(150) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE treatments (
    id                   INT          AUTO_INCREMENT PRIMARY KEY,
    doctor_id            INT          NOT NULL,
    patient_id           INT          NOT NULL,
    diagnosis            VARCHAR(300) NOT NULL,
    prescribed_treatment TEXT,
    start_date           DATE         NOT NULL,
    end_date             DATE,
    CONSTRAINT fk_treatment_doctor  FOREIGN KEY (doctor_id)
        REFERENCES doctors(id),
    CONSTRAINT fk_treatment_patient FOREIGN KEY (patient_id)
        REFERENCES patients(id)
);

CREATE TABLE treatment_medications (
    treatment_id  INT NOT NULL,
    medication_id INT NOT NULL,
    dose          VARCHAR(100),
    PRIMARY KEY (treatment_id, medication_id),
    CONSTRAINT fk_tm_treatment  FOREIGN KEY (treatment_id)
        REFERENCES treatments(id),
    CONSTRAINT fk_tm_medication FOREIGN KEY (medication_id)
        REFERENCES medications(id)
);

INSERT INTO specializations (name) VALUES
    ('General Practitioner'),
    ('Ophthalmologist'),
    ('ENT'),
    ('Cardiologist'),
    ('Dermatologist');

INSERT INTO doctors (first_name, middle_name, last_name, office, specialization_id, accepts_insurance, phone, email) VALUES
    ('Stefan',  'Georgiev',  'Popov',    '101', 1, 1, '0888100200', 'stefan.popov@hospital.bg'),
    ('Anna',    'Petrova',   'Ivanova',  '202', 2, 1, '0888300400', 'anna.ivanova@hospital.bg'),
    ('Dimitar', 'Todorov',   'Nikolov',  '303', 3, 0, '0888500600', 'dimitar.nikolov@hospital.bg'),
    ('Elena',   'Stoyanova', 'Georgieva','104', 4, 1, '0888700800', 'elena.georgieva@hospital.bg'),
    ('Hristo',  'Dimitrov',  'Vasilev',  '205', 5, 0, '0888900100', 'hristo.vasilev@hospital.bg');

INSERT INTO patients (first_name, middle_name, last_name, address, egn, date_of_birth, phone, email) VALUES
    ('Petar',    'Ivanov',    'Kolev',    '12 Rose St, Sofia',     '8501011234', '1985-01-01', '0877111222', 'petar.kolev@mail.bg'),
    ('Maria',    'Todorova',  'Stoyanova','5 Oak Ave, Plovdiv',    '9002022345', '1990-02-02', '0877333444', 'maria.stoyanova@mail.bg'),
    ('Georgi',   'Petrov',    'Hristov',  '8 Pine Rd, Varna',      '7503033456', '1975-03-03', '0877555666', 'georgi.hristov@mail.bg'),
    ('Teodora',  'Nikolova',  'Dimitrova','3 Elm Blvd, Burgas',    '9204044567', '1992-04-04', '0877777888', 'teodora.dimitrova@mail.bg'),
    ('Nikolay',  'Vasilev',   'Angelov',  '21 Maple Ln, Ruse',     '8805055678', '1988-05-05', '0877999000', 'nikolay.angelov@mail.bg');

INSERT INTO medications (name, description) VALUES
    ('Amoxicillin 500mg', 'Antibiotic'),
    ('Ibuprofen 400mg',   'Anti-inflammatory'),
    ('Lisinopril 10mg',   'ACE inhibitor for hypertension'),
    ('Loratadine 10mg',   'Antihistamine'),
    ('Metformin 850mg',   'Diabetes medication');

INSERT INTO treatments (doctor_id, patient_id, diagnosis, prescribed_treatment, start_date, end_date) VALUES
    (1, 1, 'Upper respiratory infection', 'Rest and antibiotics',         '2026-01-05', '2026-01-15'),
    (2, 2, 'Myopia',                      'Corrective lenses prescribed', '2026-01-10', NULL),
    (3, 3, 'Chronic sinusitis',           'Nasal irrigation and rest',    '2026-01-12', '2026-02-12'),
    (4, 4, 'Hypertension',                'Medication and diet changes',  '2026-02-01', NULL),
    (1, 5, 'Type 2 diabetes',             'Medication and diet plan',     '2026-02-15', NULL);

INSERT INTO treatment_medications (treatment_id, medication_id, dose) VALUES
    (1, 1, '500mg 3x daily for 10 days'),
    (1, 2, '400mg as needed'),
    (3, 2, '400mg 2x daily'),
    (4, 3, '10mg once daily'),
    (5, 5, '850mg 2x daily');
