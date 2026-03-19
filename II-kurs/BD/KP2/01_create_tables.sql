-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 1: Проектиране на база данни + CREATE TABLE заявки
-- ============================================================

CREATE DATABASE IF NOT EXISTS twitter_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE twitter_db;

-- ------------------------------------------------------------
-- Таблица: users
-- Съхранява акаунтите на потребителите - лични данни,
-- потребителско име и парола.
-- ------------------------------------------------------------
CREATE TABLE users (
    id            INT            AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)    NOT NULL UNIQUE,
    password_hash VARCHAR(255)   NOT NULL,
    email         VARCHAR(100)   NOT NULL UNIQUE,
    first_name    VARCHAR(50),
    last_name     VARCHAR(50),
    bio           TEXT,
    profile_image VARCHAR(255),
    created_at    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active     TINYINT(1)     NOT NULL DEFAULT 1
);

-- ------------------------------------------------------------
-- Таблица: tweets
-- Кратките съобщения (до 280 знака) публикувани от потребители.
-- ------------------------------------------------------------
CREATE TABLE tweets (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    user_id    INT          NOT NULL,
    content    VARCHAR(280) NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1)   NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Таблица: follows
-- Абонаменти - кой потребител следва кого (канали със съобщения).
-- ------------------------------------------------------------
CREATE TABLE follows (
    follower_id INT      NOT NULL,
    followed_id INT      NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (follower_id <> followed_id)
);

-- ------------------------------------------------------------
-- Таблица: friendships
-- Приятелска листа между потребители.
-- status: pending / accepted / blocked
-- ------------------------------------------------------------
CREATE TABLE friendships (
    id           INT      AUTO_INCREMENT PRIMARY KEY,
    requester_id INT      NOT NULL,
    addressee_id INT      NOT NULL,
    status       ENUM('pending','accepted','blocked') NOT NULL DEFAULT 'pending',
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_friendship (requester_id, addressee_id),
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (addressee_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (requester_id <> addressee_id)
);

-- ------------------------------------------------------------
-- Таблица: blocks
-- Блокирани потребители.
-- ------------------------------------------------------------
CREATE TABLE blocks (
    blocker_id INT      NOT NULL,
    blocked_id INT      NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (blocker_id, blocked_id),
    FOREIGN KEY (blocker_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (blocked_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (blocker_id <> blocked_id)
);

-- ------------------------------------------------------------
-- Таблица: profile_views
-- Проследява прегледите на профили.
-- ------------------------------------------------------------
CREATE TABLE profile_views (
    id        INT      AUTO_INCREMENT PRIMARY KEY,
    viewer_id INT      NOT NULL,
    viewed_id INT      NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (viewer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (viewed_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Таблица: likes
-- Харесвания на туити от потребители.
-- ------------------------------------------------------------
CREATE TABLE likes (
    user_id    INT      NOT NULL,
    tweet_id   INT      NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tweet_id),
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Таблица: retweets
-- Споделяния (ретуити) на туити.
-- ------------------------------------------------------------
CREATE TABLE retweets (
    user_id    INT      NOT NULL,
    tweet_id   INT      NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tweet_id),
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Таблица: direct_messages
-- Лични съобщения между потребители (комуникация).
-- ------------------------------------------------------------
CREATE TABLE direct_messages (
    id          INT      AUTO_INCREMENT PRIMARY KEY,
    sender_id   INT      NOT NULL,
    receiver_id INT      NOT NULL,
    content     TEXT     NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read     TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (sender_id)   REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (sender_id <> receiver_id)
);

-- ------------------------------------------------------------
-- Таблица: hashtags
-- Уникалните хаштагове използвани в туитите.
-- ------------------------------------------------------------
CREATE TABLE hashtags (
    id  INT         AUTO_INCREMENT PRIMARY KEY,
    tag VARCHAR(100) NOT NULL UNIQUE
);

-- ------------------------------------------------------------
-- Таблица: tweet_hashtags
-- Връзка много-към-много между туити и хаштагове.
-- ------------------------------------------------------------
CREATE TABLE tweet_hashtags (
    tweet_id   INT NOT NULL,
    hashtag_id INT NOT NULL,
    PRIMARY KEY (tweet_id, hashtag_id),
    FOREIGN KEY (tweet_id)   REFERENCES tweets(id)   ON DELETE CASCADE,
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Таблица: tweet_deletion_log
-- Одит лог за изтрити туити (попълва се от тригер).
-- ------------------------------------------------------------
CREATE TABLE tweet_deletion_log (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    tweet_id   INT          NOT NULL,
    user_id    INT          NOT NULL,
    content    VARCHAR(280) NOT NULL,
    deleted_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Таблица: user_stats
-- Кеширана статистика за потребителите (обновява се от процедура).
-- ------------------------------------------------------------
CREATE TABLE user_stats (
    user_id         INT NOT NULL PRIMARY KEY,
    tweet_count     INT NOT NULL DEFAULT 0,
    follower_count  INT NOT NULL DEFAULT 0,
    following_count INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
