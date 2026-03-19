-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 5: OUTER JOIN
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Заявка: Извеждане на ВСИЧКИ потребители и техните туити,
-- включително потребители, които все още не са публикували
-- нито един туит (резултатът им ще е NULL / 0).
-- LEFT OUTER JOIN гарантира включването на всички редове
-- от лявата таблица (users), дори без съвпадение в tweets.
-- ------------------------------------------------------------
SELECT
    u.id                        AS user_id,
    u.username,
    u.first_name,
    u.last_name,
    COUNT(t.id)                 AS tweet_count,
    MIN(t.created_at)           AS first_tweet_date,
    MAX(t.created_at)           AS last_tweet_date
FROM users u
LEFT OUTER JOIN tweets t ON u.id = t.user_id AND t.is_deleted = 0
GROUP BY u.id, u.username, u.first_name, u.last_name
ORDER BY tweet_count DESC;
