-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 6: Вложен SELECT (подзаявка)
-- ============================================================
-- Извежда потребителите, които са изпратили повече съобщения
-- от средния брой изпратени съобщения за всички потребители.
-- ============================================================

USE messaging_system;

SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
    u.username,
    (
        SELECT COUNT(*)
        FROM messages m
        WHERE m.sender_id = u.user_id
    ) AS messages_sent
FROM users u
WHERE (
    SELECT COUNT(*)
    FROM messages m
    WHERE m.sender_id = u.user_id
) > (
    SELECT AVG(msg_count)
    FROM (
        SELECT COUNT(*) AS msg_count
        FROM messages
        GROUP BY sender_id
    ) AS per_user_counts
)
ORDER BY messages_sent DESC;
