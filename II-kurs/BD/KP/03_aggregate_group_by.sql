-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 3: Агрегатна функция и GROUP BY
-- ============================================================
-- Брой изпратени съобщения на потребител.
-- Показва само тези, изпратили повече от 1 съобщение.
-- ============================================================

USE messaging_system;

SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
    u.username,
    COUNT(m.message_id)  AS total_sent,
    MIN(m.sent_at)       AS first_message_at,
    MAX(m.sent_at)       AS last_message_at
FROM users u
JOIN messages m ON m.sender_id = u.user_id
GROUP BY u.user_id, u.first_name, u.last_name, u.username
HAVING COUNT(m.message_id) > 1
ORDER BY total_sent DESC;
