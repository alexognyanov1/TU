-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 6: Вложен SELECT (подзаявка)
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Заявка: Извеждане на потребителите, чиито туити са получили
-- повече харесвания от средния брой харесвания на всички туити.
-- Използват се два нива на вложени подзаявки:
--   1. Вътрешна подзаявка изчислява средния брой харесвания.
--   2. Средна подзаявка събира харесванията за конкретен потребител.
-- ------------------------------------------------------------
SELECT
    u.username,
    u.first_name,
    u.last_name,
    (
        SELECT COUNT(*)
        FROM likes l
        JOIN tweets t ON l.tweet_id = t.id
        WHERE t.user_id = u.id
          AND t.is_deleted = 0
    ) AS total_likes_received
FROM users u
WHERE (
    -- Общо харесвания за този потребител
    SELECT COUNT(*)
    FROM likes l
    JOIN tweets t ON l.tweet_id = t.id
    WHERE t.user_id = u.id
      AND t.is_deleted = 0
) > (
    -- Средно харесвания за ВСЕКИ потребител
    SELECT AVG(likes_per_user)
    FROM (
        SELECT COUNT(l2.tweet_id) AS likes_per_user
        FROM users u2
        LEFT JOIN tweets t2  ON u2.id  = t2.user_id AND t2.is_deleted = 0
        LEFT JOIN likes  l2  ON t2.id  = l2.tweet_id
        GROUP BY u2.id
    ) AS per_user_stats
)
ORDER BY total_likes_received DESC;
