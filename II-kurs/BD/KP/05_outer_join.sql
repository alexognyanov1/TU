-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 5: OUTER JOIN
-- ============================================================
-- Извежда всички потребители и броя на получените съобщения.
-- LEFT JOIN гарантира, че потребители БЕЗ получени съобщения
-- също се показват (с 0).
-- ============================================================

USE messaging_system;

SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
    u.username,
    COUNT(m.message_id) AS received_messages
FROM users u
LEFT JOIN messages m
    ON m.receiver_id = u.user_id
    AND m.is_deleted_by_receiver = 0
GROUP BY u.user_id, u.first_name, u.last_name, u.username
ORDER BY received_messages DESC;
