-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 4: INNER JOIN
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Заявка: Извеждане на всички лични съобщения заедно с
-- имената на изпращача и получателя (INNER JOIN към users
-- два пъти - веднъж за sender, веднъж за receiver).
-- Показват се само съобщения между реално съществуващи
-- и двете страни (именно затова INNER JOIN е подходящ).
-- ------------------------------------------------------------
SELECT
    dm.id             AS message_id,
    sender.username   AS from_user,
    sender.first_name AS from_first_name,
    receiver.username AS to_user,
    receiver.first_name AS to_first_name,
    dm.content,
    dm.created_at,
    dm.is_read
FROM direct_messages dm
INNER JOIN users AS sender   ON dm.sender_id   = sender.id
INNER JOIN users AS receiver ON dm.receiver_id = receiver.id
ORDER BY dm.created_at ASC;
