-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 1: CREATE TABLE заявки (MySQL)
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
('Иван',      'Петров',    'ул. Витоша 1, София',                   '0888111222', 'ivan@example.com',      'ivan_p',      SHA2('pass1234', 256), 'Обичам планината.'),
('Мария',     'Иванова',   'бул. Христо Ботев 5, Пловдив',          '0877333444', 'maria@example.com',     'maria_i',     SHA2('secr3t',   256), 'Програмист и геймър.'),
('Георги',    'Стоянов',   'ул. Оборище 12, Варна',                 '0866555666', 'georgi@example.com',    'gosho99',     SHA2('qwerty',   256), NULL),
('Петя',      'Димитрова', 'ул. Граф Игнатиев 3, София',            '0855777888', 'petya@example.com',     'petya_d',     SHA2('abc123',   256), 'Обичам котки.'),
('Стефан',    'Николов',   'ул. Ракovski 20, Бургас',               '0844999000', 'stefan@example.com',    'stefan_n',    SHA2('mypass',   256), 'Музикант.'),
('Елена',     'Василева',  'ул. Цар Симеон 8, София',               '0833222111', 'elena@example.com',     'elena_v',     SHA2('elena99',  256), 'Пътешественик и фотограф.'),
('Димитър',   'Костов',    'бул. Сливница 44, Монтана',             '0822444555', 'dimitar@example.com',   'dido_k',      SHA2('dido2024', 256), 'Фен на технологиите.'),
('Анна',      'Георгиева', 'ул. Патриарх Евтимий 2, Стара Загора', '0811666777', 'anna@example.com',      'anna_g',      SHA2('annna!',   256), 'Обичам готвенето.'),
('Николай',   'Тодоров',   'кв. Лозенец 15, София',                '0800888999', 'nikolay@example.com',   'niki_t',      SHA2('niki007',  256), NULL),
('Силвия',    'Маринова',  'ул. Шипка 3, Казанлък',                 '0799111333', 'silviya@example.com',   'silviya_m',   SHA2('s!lv1ya',  256), 'Учителка по математика.'),
('Красимир',  'Янков',     'ул. Сердика 7, Плевен',                 '0788222444', 'krasimir@example.com',  'krasi_y',     SHA2('kr@si99',  256), 'Програмист. Обичам хакатони.'),
('Теодора',   'Пенева',    'бул. Черни връх 21, София',             '0777333555', 'teodora@example.com',   'teddy_p',     SHA2('teddy123', 256), 'Студентка по право.'),
('Борислав',  'Миков',     'ул. Хан Аспарух 4, Шумен',             '0766444666', 'borislav@example.com',  'boko_m',      SHA2('b0k0!',    256), NULL),
('Виктория',  'Стефанова', 'ул. Алабин 10, София',                  '0755555777', 'viktoriya@example.com', 'viki_s',      SHA2('v1k!2024', 256), 'Журналист. Следя технологиите.'),
('Калоян',    'Илиев',     'бул. Ал. Стамболийски 33, Перник',      '0744666888', 'kaloyan@example.com',   'kalo_i',      SHA2('kal0yan',  256), 'Доброволец и планинар.'),
('Надежда',   'Христова',  'ул. Цар Асен 2, Велико Търново',        '0733777999', 'nadezhda@example.com',  'nadya_h',     SHA2('n@dya!',   256), 'Организатор на събития.'),
('Радослав',  'Генов',     'ул. Ген. Скобелев 15, Пазарджик',       '0722888000', 'radoslav@example.com',  'rado_g',      SHA2('r@do2024', 256), NULL),
('Ясен',      'Петков',    'ул. Братя Миладинови 8, Сливен',        '0711999111', 'yasen@example.com',     'yasen_p',     SHA2('y@sen!',   256), 'Предприемач и ментор.'),
('Кристина',  'Колева',    'бул. Патриарх Евтимий 5, София',        '0700111222', 'kristina@example.com',  'kris_k',      SHA2('kr1st!na', 256), 'Дизайнер на интериори.'),
('Момчил',    'Захариев',  'ул. Цариброд 22, Видин',                '0699222333', 'momchil@example.com',   'momcho_z',    SHA2('m0mch0!',  256), 'Финансов анализатор.');

INSERT INTO messages (sender_id, receiver_id, content, read_at) VALUES
-- Група 1
( 1,  2, 'Здравей Мария! Как си?',                                NOW()),
( 2,  1, 'Добре, благодаря! Ти как си?',                          NOW()),
( 1,  2, 'И аз добре. Имаш ли планове за уикенда?',               NULL),
( 2,  1, 'Ще ходим на гости. Ти?',                                NOW()),
( 1,  2, 'Може да ходим на кино. Интересуваш ли се?',             NOW()),
( 2,  1, 'Да, звучи добре! Кой филм?',                            NOW()),
( 1,  2, 'Новият Marvel. В 19:00 ч.',                             NOW()),
( 2,  1, 'Перфектно! Ще бъда там.',                               NOW()),
-- Група 2
( 1,  3, 'Георги, ще излизаш ли утре?',                           NOW()),
( 3,  1, 'Да, ще съм там. В колко часа?',                         NULL),
( 1,  3, 'По обяд, 12:30 на площада.',                            NOW()),
( 3,  1, 'Добре, ще дойда.',                                      NOW()),
( 1,  3, 'Чудесно, лека нощ!',                                    NOW()),
-- Група 3
( 2,  4, 'Петя, видя ли новия проект?',                           NOW()),
( 4,  2, 'Да, много е интересен!',                                NOW()),
( 2,  4, 'Смяташ ли да кандидатстваш?',                           NULL),
( 4,  2, 'Обмислям го. Ти?',                                      NOW()),
( 2,  4, 'Да, ще изпратя документите утре.',                       NOW()),
( 4,  2, 'Успех! Надявам се да ни вземат и двете.',               NOW()),
-- Група 4
( 5,  6, 'Елена, здравей! Как е работата?',                       NOW()),
( 6,  5, 'Много натоварено напоследък!',                           NULL),
( 5,  6, 'Нужна ли ти е помощ с нещо?',                           NOW()),
( 6,  5, 'Всъщност да. Можеш ли да прегледаш доклада?',           NOW()),
( 5,  6, 'Разбира се, изпрати ми го.',                             NOW()),
( 6,  5, 'Изпратих го на имейл. Благодаря!',                      NOW()),
( 5,  6, 'Прегледах го. Много добра работа!',                      NOW()),
-- Група 5
( 7,  2, 'Мария, имаш ли препоръка за курс по Python?',           NOW()),
( 2,  7, 'Препоръчвам курса в Coursera!',                         NULL),
( 7,  2, 'Безплатен ли е?',                                       NOW()),
( 2,  7, 'Има и безплатен вариант с ограничения.',                 NOW()),
( 7,  2, 'Благодаря! Ще го разгледам.',                            NOW()),
-- Група 6
( 8,  3, 'Георги, ела на кафе?',                                  NOW()),
( 3,  8, 'С удоволствие! Кога?',                                  NOW()),
( 8,  3, 'Утре следобед около 15:00.',                             NOW()),
( 3,  8, 'Добре, ще бъда там!',                                   NOW()),
-- Група 7
( 9,  5, 'Стефане, свири ли на концерта в петък?',                NOW()),
( 5,  9, 'Да, ела задължително!',                                  NOW()),
( 9,  5, 'В колко часа започва?',                                  NOW()),
( 5,  9, 'В 20:00. Вход е свободен.',                              NOW()),
( 9,  5, 'Страхотно, ще доведа и Силвия!',                        NOW()),
( 5,  9, 'Добре дошли!',                                           NOW()),
-- Група 8
(10,  4, 'Петя, имаш ли рецепта за баница?',                      NOW()),
( 4, 10, 'Разбира се! Ще ти пратя сега.',                         NOW()),
(10,  4, 'Благодаря, много си мила!',                              NULL),
( 4, 10, 'Моля! Приятно готвене!',                                 NOW()),
(10,  4, 'Стана много вкусна!',                                    NOW()),
-- Група 9
(11,  1, 'Иване, добро утро!',                                     NOW()),
( 1, 11, 'Добро утро, Красимире!',                                 NOW()),
(11,  1, 'Ще участваш ли в хакатона следващата седмица?',          NULL),
( 1, 11, 'Да, вече съм записан. Ти?',                              NOW()),
-- Група 10
(12,  2, 'Мария, кога е следващото занятие?',                      NOW()),
( 2, 12, 'В сряда от 18:00.',                                     NOW()),
(12,  2, 'Ще има ли нов материал?',                                NOW()),
( 2, 12, 'Да, започваме нова глава.',                              NOW()),
(12,  2, 'Ще подготвя предварително. Благодаря!',                  NULL),
-- Група 11
(13,  6, 'Елена, получи ли файловете?',                            NOW()),
( 6, 13, 'Да, благодаря! Всичко е наред.',                        NOW()),
(13,  6, 'Имаш ли въпроси по тях?',                               NOW()),
( 6, 13, 'Засега не. Ще се свържа при нужда.',                    NOW()),
-- Група 12
(14,  7, 'Димитре, виждал ли си тази новина?',                    NOW()),
( 7, 14, 'Не, каква е?',                                           NOW()),
(14,  7, 'За новия AI инструмент на Google!',                      NOW()),
( 7, 14, 'Сега го прочетох. Впечатляващо!',                       NOW()),
(14,  7, 'Нали! Светът се мени толкова бързо.',                   NOW()),
-- Група 13
(15,  8, 'Анна, здравей! Как е детето?',                          NOW()),
( 8, 15, 'Много добре, расте бързо!',                              NOW()),
(15,  8, 'Пожелавам ви здраве!',                                   NOW()),
( 8, 15, 'Благодаря, Калояне!',                                   NOW()),
-- Група 14
(16,  9, 'Николай, ще дойдеш ли на срещата?',                     NOW()),
( 9, 16, 'Да, ще бъда там.',                                      NOW()),
(16,  9, 'Страхотно! В конферентната зала.',                       NULL),
( 9, 16, 'В колко часа?',                                          NOW()),
(16,  9, 'В 10:00 сутринта.',                                     NOW()),
-- Група 15
(17, 10, 'Силвия, как вървят уроците?',                           NOW()),
(10, 17, 'Много добре! Децата са страхотни.',                     NULL),
(17, 10, 'Радвам се! Продължавай така.',                           NOW()),
(10, 17, 'Благодаря за подкрепата!',                              NOW()),
-- Група 16
(18, 11, 'Красимире, имаш ли свободно утре?',                     NOW()),
(11, 18, 'Да, след обяд.',                                         NOW()),
(18, 11, 'Можем ли да се видим за проекта?',                       NULL),
(11, 18, 'Разбира се. В 14:00?',                                   NOW()),
(18, 11, 'Перфектно, ще те чакам.',                               NOW()),
-- Група 17
(19, 12, 'Теодора, успя ли с доклада?',                           NULL),
(12, 19, 'Да, предадох го навреме!',                               NOW()),
(19, 12, 'Браво! Беше много труден.',                              NULL),
(12, 19, 'Да, но се справих!',                                    NOW()),
-- Група 18
(20, 13, 'Борисаве, как е в новата компания?',                    NULL),
(13, 20, 'Страхотно! Много добра среда.',                         NOW()),
(20, 13, 'Радвам се за теб!',                                     NULL),
(13, 20, 'Благодаря! Как е при теб?',                             NULL),
-- Група 19
( 1,  4, 'Петя, имаш ли контакта на Мария?',                     NOW()),
( 4,  1, 'Да, ще ти го изпратя веднага.',                         NOW()),
(15,  3, 'Георги, запознати ли сме се?',                          NULL),
(17, 20, 'Момчил, добре дошъл в групата!',                        NULL),
(19,  5, 'Стефане, имате ли места на концерта?',                  NULL),
-- Група 20
( 2,  3, 'Георги, всичко наред ли е с проекта?',                  NULL),
( 3,  5, 'Стефане, нужна ли ти е помощ с музиката?',              NULL),
( 6,  8, 'Анна, ела на разходка с нас!',                          NULL),
(14,  1, 'Иване, поздрави от Виктория!',                          NULL),
(20,  7, 'Димитре, интересуваш ли се от инвестиции?',             NULL);

INSERT INTO friendships (requester_id, addressee_id, status) VALUES
( 1,  2, 'accepted'),
( 1,  3, 'accepted'),
( 4,  1, 'accepted'),
( 5,  1, 'accepted'),
( 2,  5, 'pending'),
( 3,  4, 'rejected'),
( 6,  1, 'accepted'),
( 6,  2, 'accepted'),
( 7,  2, 'accepted'),
( 7,  9, 'accepted'),
( 8,  3, 'pending'),
( 9,  5, 'accepted'),
(10,  4, 'accepted'),
(10,  1, 'accepted'),
( 6,  8, 'pending'),
( 3,  9, 'rejected'),
( 5,  7, 'pending'),
( 4,  6, 'accepted'),
(11,  1, 'accepted'),
(12,  2, 'accepted'),
(13,  6, 'accepted'),
(14,  7, 'accepted'),
(15,  8, 'accepted'),
(16,  9, 'accepted'),
(17, 10, 'accepted'),
(18, 11, 'accepted'),
(19, 12, 'accepted'),
(20, 13, 'accepted'),
(14,  2, 'pending'),
(15,  3, 'pending'),
(16,  4, 'rejected'),
(17,  5, 'pending'),
(20,  1, 'rejected');

INSERT INTO blocks (blocker_id, blocked_id) VALUES
(2,  3),
(4,  5),
(3,  9),
(7,  10),
(1,  8),
(6,  7);

INSERT INTO profile_views (viewer_id, viewed_id) VALUES
(1,  2),  (1,  3),  (2,  1),  (3,  1),  (4,  2),  (5,  1),  (1,  4),  (2,  5),
(6,  1),  (6,  2),  (7,  2),  (7,  9),  (8,  3),  (9,  5),  (10, 4),  (10, 1),
(3,  6),  (4,  7),  (5,  8),  (1,  9),  (2,  10), (6,  10), (9,  1),  (8,  6),
(7,  3),  (10, 5),  (3,  7),  (4,  9),  (5,  10), (1,  10);

INSERT INTO communication_logs (actor_id, target_id, action_type, details) VALUES
-- Заявки за приятелство и приемания
( 1,  2, 'friend_request_sent',      NULL),
( 2,  1, 'friend_request_accepted',  NULL),
( 1,  3, 'friend_request_sent',      NULL),
( 3,  1, 'friend_request_accepted',  NULL),
( 4,  1, 'friend_request_sent',      NULL),
( 1,  4, 'friend_request_accepted',  NULL),
( 5,  1, 'friend_request_sent',      NULL),
( 1,  5, 'friend_request_accepted',  NULL),
( 6,  1, 'friend_request_sent',      NULL),
( 1,  6, 'friend_request_accepted',  NULL),
( 6,  2, 'friend_request_sent',      NULL),
( 2,  6, 'friend_request_accepted',  NULL),
( 7,  2, 'friend_request_sent',      NULL),
( 2,  7, 'friend_request_accepted',  NULL),
( 9,  5, 'friend_request_sent',      NULL),
( 5,  9, 'friend_request_accepted',  NULL),
(10,  4, 'friend_request_sent',      NULL),
( 4, 10, 'friend_request_accepted',  NULL),
(10,  1, 'friend_request_sent',      NULL),
( 1, 10, 'friend_request_accepted',  NULL),
(11,  1, 'friend_request_sent',      NULL),
( 1, 11, 'friend_request_accepted',  NULL),
(18, 11, 'friend_request_sent',      NULL),
(11, 18, 'friend_request_accepted',  NULL),
(19, 12, 'friend_request_sent',      NULL),
(12, 19, 'friend_request_accepted',  NULL),
-- Блокирания
( 2,  3, 'user_blocked',             NULL),
( 4,  5, 'user_blocked',             NULL),
( 3,  9, 'user_blocked',             NULL),
( 7, 10, 'user_blocked',             NULL),
( 1,  8, 'user_blocked',             NULL),
( 6,  7, 'user_blocked',             NULL),
-- Изпратени съобщения (представителна извадка)
( 1,  2, 'message_sent',             'message_id=1'),
( 2,  1, 'message_sent',             'message_id=2'),
( 1,  2, 'message_sent',             'message_id=3'),
( 2,  1, 'message_sent',             'message_id=4'),
( 1,  3, 'message_sent',             'message_id=9'),
( 2,  4, 'message_sent',             'message_id=14'),
( 5,  6, 'message_sent',             'message_id=20'),
( 7,  2, 'message_sent',             'message_id=27'),
( 9,  5, 'message_sent',             'message_id=36'),
(10,  4, 'message_sent',             'message_id=42'),
(11,  1, 'message_sent',             'message_id=47'),
(12,  2, 'message_sent',             'message_id=51'),
(16,  9, 'message_sent',             'message_id=69'),
(18, 11, 'message_sent',             'message_id=78'),
(20, 13, 'message_sent',             'message_id=87'),
-- Прочетени съобщения
( 2,  1, 'message_read',             'message_id=1'),
( 1,  2, 'message_read',             'message_id=2'),
( 3,  1, 'message_read',             'message_id=9'),
( 5,  9, 'message_read',             'message_id=36'),
( 4, 10, 'message_read',             'message_id=42'),
( 1, 11, 'message_read',             'message_id=47'),
-- Прегледани профили
( 1,  2, 'profile_viewed',           NULL),
( 2,  1, 'profile_viewed',           NULL),
( 6,  1, 'profile_viewed',           NULL),
( 7,  9, 'profile_viewed',           NULL),
( 8,  3, 'profile_viewed',           NULL),
(11,  1, 'profile_viewed',           NULL),
(14,  7, 'profile_viewed',           NULL),
(16,  9, 'profile_viewed',           NULL),
(19, 12, 'profile_viewed',           NULL);

-- Изпратени/получени са преброени от съобщенията по-горе (100 общо)
INSERT INTO user_message_stats (user_id, total_messages_sent, total_messages_received) VALUES
( 1, 10, 10),
( 2, 12, 13),
( 3,  5,  7),
( 4,  6,  7),
( 5,  7,  8),
( 6,  6,  6),
( 7,  5,  6),
( 8,  4,  5),
( 9,  5,  6),
(10,  5,  4),
(11,  4,  5),
(12,  5,  4),
(13,  4,  4),
(14,  4,  2),
(15,  3,  2),
(16,  3,  2),
(17,  3,  2),
(18,  3,  2),
(19,  3,  2),
(20,  3,  3);
