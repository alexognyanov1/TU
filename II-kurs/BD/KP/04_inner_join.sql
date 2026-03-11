-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 4: INNER JOIN
-- ============================================================
-- Извежда всички съобщения заедно с имената на подателя
-- и получателя (само съобщения между двама съществуващи
-- потребители – INNER JOIN гарантира това).
-- ============================================================

USE messaging_system;

SELECT
    m.message_id,
    CONCAT(s.first_name, ' ', s.last_name) AS sender_name,
    s.username                              AS sender_username,
    CONCAT(r.first_name, ' ', r.last_name) AS receiver_name,
    r.username                              AS receiver_username,
    LEFT(m.content, 60)                    AS message_preview,
    m.sent_at,
    IF(m.read_at IS NOT NULL, 'Прочетено', 'Непрочетено') AS read_status
FROM messages m
INNER JOIN users s ON s.user_id = m.sender_id
INNER JOIN users r ON r.user_id = m.receiver_id
ORDER BY m.sent_at DESC;
