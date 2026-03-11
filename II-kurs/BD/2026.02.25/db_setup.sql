-- =======================
-- Table: students
-- =======================
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    grade INT,
    class VARCHAR(5),
    date_of_birth DATE,
    email VARCHAR(100) UNIQUE
) ENGINE=InnoDB;


-- =======================
-- Table: club_types
-- =======================
CREATE TABLE IF NOT EXISTS club_types (
    club_type_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    description TEXT
) ENGINE=InnoDB;


-- =======================
-- Table: clubs
-- =======================
CREATE TABLE IF NOT EXISTS clubs (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    club_type_id INT,
    club_name VARCHAR(100),
    start_date DATE,
    INDEX idx_club_type_id (club_type_id)
) ENGINE=InnoDB;


-- =======================
-- Table: trainers
-- =======================
CREATE TABLE IF NOT EXISTS trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    hire_date DATE
) ENGINE=InnoDB;


-- =======================
-- Table: `groups`
-- =======================
CREATE TABLE IF NOT EXISTS `groups` (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    club_id INT,
    trainer_id INT,
    group_name VARCHAR(100),
    day_of_week ENUM(
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ),
    start_time TIME,
    end_time TIME,
    max_students INT,
    INDEX idx_club_id (club_id),
    INDEX idx_trainer_id (trainer_id)
) ENGINE=InnoDB;


-- =======================
-- Table: enrollments
-- =======================
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    group_id INT,
    enrollment_date DATE,
    INDEX idx_student_id (student_id),
    INDEX idx_group_id (group_id)
) ENGINE=InnoDB;


-- =======================
-- Foreign Keys (safe add)
-- =======================

-- clubs → club_types
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'clubs'
      AND CONSTRAINT_NAME = 'fk_clubs_club_type'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE clubs
     ADD CONSTRAINT fk_clubs_club_type
     FOREIGN KEY (club_type_id)
     REFERENCES club_types(club_type_id)
     ON DELETE CASCADE;',
    'SELECT 1;'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


-- groups → clubs
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'groups'
      AND CONSTRAINT_NAME = 'fk_groups_club'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE `groups`
     ADD CONSTRAINT fk_groups_club
     FOREIGN KEY (club_id)
     REFERENCES clubs(club_id)
     ON DELETE CASCADE;',
    'SELECT 1;'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


-- groups → trainers
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'groups'
      AND CONSTRAINT_NAME = 'fk_groups_trainer'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE `groups`
     ADD CONSTRAINT fk_groups_trainer
     FOREIGN KEY (trainer_id)
     REFERENCES trainers(trainer_id)
     ON DELETE SET NULL;',
    'SELECT 1;'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


-- enrollments → groups
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'enrollments'
      AND CONSTRAINT_NAME = 'fk_enrollments_group'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE enrollments
     ADD CONSTRAINT fk_enrollments_group
     FOREIGN KEY (group_id)
     REFERENCES `groups`(group_id)
     ON DELETE CASCADE;',
    'SELECT 1;'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;


-- enrollments → students
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'enrollments'
      AND CONSTRAINT_NAME = 'fk_enrollments_student'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE enrollments
     ADD CONSTRAINT fk_enrollments_student
     FOREIGN KEY (student_id)
     REFERENCES students(student_id)
     ON DELETE CASCADE;',
    'SELECT 1;'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;