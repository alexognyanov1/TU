-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 1: CREATE TABLE заявки (MySQL)
-- ============================================================
-- ER диаграма (текстово описание):
--
--  users ──────────────────────────────────────────┐
--    │                                              │
--    │ 1:N (sender/receiver)                        │
--    ▼                                              │
--  messages                                         │
--                                                   │
--  users ──── friendships ──── users                │
--   (requester_id)  (addressee_id)                  │
--                                                   │
--  users ──── blocks ──── users                     │
--   (blocker_id)  (blocked_id)                      │
--                                                   │
--  users ──── profile_views ──── users              │
--   (viewer_id)    (viewed_id)                      │
--                                                   │
--  users ──── communication_logs ──────────────────-┘
--   (actor_id / target_id)
--
--  users ──── user_message_stats  (1:1)
-- ============================================================

CREATE DATABASE IF NOT EXISTS messaging_system
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE messaging_system;

-- -----------------------------------------------------------
-- Таблица: users
-- Съдържа личните данни и акаунт информацията на потребителите
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id          INT             AUTO_INCREMENT PRIMARY KEY,
    first_name       VARCHAR(50)     NOT NULL,
    last_name        VARCHAR(50)     NOT NULL,
    address          VARCHAR(255),
    phone            VARCHAR(20),
    email            VARCHAR(100)    NOT NULL UNIQUE,
    username         VARCHAR(50)     NOT NULL UNIQUE,
    password_hash    VARCHAR(255)    NOT NULL,
    bio              TEXT,
    profile_picture  VARCHAR(500),
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login       DATETIME,
    is_active        TINYINT(1)      NOT NULL DEFAULT 1
);

-- -----------------------------------------------------------
-- Таблица: messages
-- Директни съобщения между двама потребители
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
    message_id               INT          AUTO_INCREMENT PRIMARY KEY,
    sender_id                INT          NOT NULL,
    receiver_id              INT          NOT NULL,
    content                  TEXT         NOT NULL,
    sent_at                  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at                  DATETIME,
    is_deleted_by_sender     TINYINT(1)   NOT NULL DEFAULT 0,
    is_deleted_by_receiver   TINYINT(1)   NOT NULL DEFAULT 0,
    FOREIGN KEY (sender_id)   REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- Таблица: friendships
-- Заявки за приятелство и установени приятелски връзки
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS friendships (
    friendship_id   INT     AUTO_INCREMENT PRIMARY KEY,
    requester_id    INT     NOT NULL,
    addressee_id    INT     NOT NULL,
    status          ENUM('pending', 'accepted', 'rejected') NOT NULL DEFAULT 'pending',
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (addressee_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY uq_friendship (requester_id, addressee_id)
);

-- -----------------------------------------------------------
-- Таблица: blocks
-- Блокирани потребители
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS blocks (
    block_id    INT      AUTO_INCREMENT PRIMARY KEY,
    blocker_id  INT      NOT NULL,
    blocked_id  INT      NOT NULL,
    blocked_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blocker_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (blocked_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY uq_block (blocker_id, blocked_id)
);

-- -----------------------------------------------------------
-- Таблица: profile_views
-- История на прегледаните профили
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS profile_views (
    view_id    INT      AUTO_INCREMENT PRIMARY KEY,
    viewer_id  INT      NOT NULL,
    viewed_id  INT      NOT NULL,
    viewed_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (viewer_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (viewed_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- Таблица: communication_logs
-- Пълни логове на всички комуникационни събития
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS communication_logs (
    log_id       INT          AUTO_INCREMENT PRIMARY KEY,
    actor_id     INT          NOT NULL,
    target_id    INT,
    action_type  ENUM(
                    'message_sent',
                    'message_read',
                    'friend_request_sent',
                    'friend_request_accepted',
                    'friend_request_rejected',
                    'user_blocked',
                    'user_unblocked',
                    'profile_viewed'
                 ) NOT NULL,
    details      TEXT,
    logged_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (actor_id)  REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- -----------------------------------------------------------
-- Таблица: user_message_stats
-- Агрегирана статистика за изпратени/получени съобщения (1:1 с users)
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_message_stats (
    stat_id                  INT      AUTO_INCREMENT PRIMARY KEY,
    user_id                  INT      NOT NULL UNIQUE,
    total_messages_sent      INT      NOT NULL DEFAULT 0,
    total_messages_received  INT      NOT NULL DEFAULT 0,
    last_updated             DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- Примерни данни
-- -----------------------------------------------------------
INSERT INTO users (first_name, last_name, address, phone, email, username, password_hash, bio) VALUES
('Иван',    'Петров',   'ул. Витоша 1, София',       '0888111222', 'ivan@example.com',   'ivan_p',    SHA2('pass1234', 256), 'Обичам планината.'),
('Мария',   'Иванова',  'бул. Христо Ботев 5, Пловдив','0877333444','maria@example.com',  'maria_i',   SHA2('secr3t',  256), 'Програмист и геймър.'),
('Георги',  'Стоянов',  'ул. Оборище 12, Варна',     '0866555666', 'georgi@example.com', 'gosho99',   SHA2('qwerty',  256), NULL),
('Петя',    'Димитрова','ул. Граф Игнатиев 3, София', '0855777888', 'petya@example.com',  'petya_d',   SHA2('abc123',  256), 'Обичам котки.'),
('Стефан',  'Николов',  'ул. Ракovski 20, Бургас',   '0844999000', 'stefan@example.com', 'stefan_n',  SHA2('mypass',  256), 'Музикант.');

INSERT INTO messages (sender_id, receiver_id, content, read_at) VALUES
(1, 2, 'Здравей Мария! Как си?',                     NOW()),
(2, 1, 'Здравей Иване! Добре съм, благодаря!',        NOW()),
(1, 3, 'Георги, ще излизаш ли утре?',                 NULL),
(3, 1, 'Да, ще съм там.',                             NOW()),
(4, 2, 'Мария, видя ли новия проект?',                NOW()),
(2, 4, 'Да, много е интересен!',                      NULL),
(1, 2, 'Ще се видим ли тази седмица?',                NULL),
(5, 1, 'Иване, имаш ли малко свободно време?',        NOW()),
(1, 5, 'Разбира се! Кажи.',                           NOW()),
(3, 4, 'Петя, поздрави!',                             NULL);

INSERT INTO friendships (requester_id, addressee_id, status) VALUES
(1, 2, 'accepted'),
(1, 3, 'accepted'),
(4, 1, 'accepted'),
(5, 1, 'accepted'),
(2, 5, 'pending'),
(3, 4, 'rejected');

INSERT INTO blocks (blocker_id, blocked_id) VALUES
(2, 3),
(4, 5);

INSERT INTO profile_views (viewer_id, viewed_id) VALUES
(1, 2), (1, 3), (2, 1), (3, 1), (4, 2), (5, 1), (1, 4), (2, 5);

INSERT INTO communication_logs (actor_id, target_id, action_type, details) VALUES
(1, 2, 'message_sent',             'message_id=1'),
(2, 1, 'message_sent',             'message_id=2'),
(1, 2, 'friend_request_sent',      NULL),
(2, 1, 'friend_request_accepted',  NULL),
(2, 3, 'user_blocked',             NULL),
(1, 3, 'message_sent',             'message_id=3'),
(4, 5, 'user_blocked',             NULL),
(1, 2, 'profile_viewed',           NULL),
(2, 1, 'message_read',             'message_id=1');

INSERT INTO user_message_stats (user_id, total_messages_sent, total_messages_received) VALUES
(1, 4, 2),
(2, 3, 3),
(3, 2, 1),
(4, 1, 2),
(5, 1, 2);
