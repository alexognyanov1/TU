-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 7: едновременно JOIN и агрегатна функция
-- ============================================================
-- За всяка двойка приятели (статус 'accepted') показва
-- общия брой съобщения, разменени между тях.
-- ============================================================

USE messaging_system;

SELECT
    CONCAT(u1.first_name, ' ', u1.last_name) AS user1_name,
    u1.username                               AS user1_username,
    CONCAT(u2.first_name, ' ', u2.last_name) AS user2_name,
    u2.username                               AS user2_username,
    COUNT(m.message_id)                       AS total_messages_exchanged
FROM friendships f
INNER JOIN users u1 ON u1.user_id = f.requester_id
INNER JOIN users u2 ON u2.user_id = f.addressee_id
LEFT JOIN messages m
    ON (m.sender_id   = f.requester_id AND m.receiver_id = f.addressee_id)
    OR (m.sender_id   = f.addressee_id AND m.receiver_id = f.requester_id)
WHERE f.status = 'accepted'
GROUP BY f.friendship_id, u1.user_id, u1.first_name, u1.last_name, u1.username,
         u2.user_id, u2.first_name, u2.last_name, u2.username
ORDER BY total_messages_exchanged DESC;
