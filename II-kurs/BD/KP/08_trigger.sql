-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 8: Тригер
-- ============================================================
-- Тригер 1: след INSERT в messages автоматично се добавя
--   запис в communication_logs и се обновява user_message_stats.
--
-- Тригер 2: след UPDATE на friendships (при приемане/отхвърляне)
--   се добавя запис в communication_logs.
-- ============================================================

USE messaging_system;

DELIMITER $$

-- -----------------------------------------------------------
-- Тригер: trg_after_message_insert
-- Логва изпращане на съобщение и обновява статистиката.
-- -----------------------------------------------------------
DROP TRIGGER IF EXISTS trg_after_message_insert$$

CREATE TRIGGER trg_after_message_insert
AFTER INSERT ON messages
FOR EACH ROW
BEGIN
    -- Лог в communication_logs
    INSERT INTO communication_logs (actor_id, target_id, action_type, details)
    VALUES (
        NEW.sender_id,
        NEW.receiver_id,
        'message_sent',
        CONCAT('message_id=', NEW.message_id)
    );

    -- Обнови статистиката за подателя
    INSERT INTO user_message_stats (user_id, total_messages_sent, total_messages_received)
    VALUES (NEW.sender_id, 1, 0)
    ON DUPLICATE KEY UPDATE total_messages_sent = total_messages_sent + 1;

    -- Обнови статистиката за получателя
    INSERT INTO user_message_stats (user_id, total_messages_sent, total_messages_received)
    VALUES (NEW.receiver_id, 0, 1)
    ON DUPLICATE KEY UPDATE total_messages_received = total_messages_received + 1;
END$$

-- -----------------------------------------------------------
-- Тригер: trg_after_friendship_update
-- Логва приемане или отхвърляне на заявка за приятелство.
-- -----------------------------------------------------------
DROP TRIGGER IF EXISTS trg_after_friendship_update$$

CREATE TRIGGER trg_after_friendship_update
AFTER UPDATE ON friendships
FOR EACH ROW
BEGIN
    IF NEW.status = 'accepted' AND OLD.status != 'accepted' THEN
        INSERT INTO communication_logs (actor_id, target_id, action_type, details)
        VALUES (
            NEW.addressee_id,
            NEW.requester_id,
            'friend_request_accepted',
            CONCAT('friendship_id=', NEW.friendship_id)
        );
    ELSEIF NEW.status = 'rejected' AND OLD.status != 'rejected' THEN
        INSERT INTO communication_logs (actor_id, target_id, action_type, details)
        VALUES (
            NEW.addressee_id,
            NEW.requester_id,
            'friend_request_rejected',
            CONCAT('friendship_id=', NEW.friendship_id)
        );
    END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------------
-- Демонстрация на тригерите
-- -----------------------------------------------------------

-- Изпращане на ново съобщение → тригерът записва лог и обновява stats
INSERT INTO messages (sender_id, receiver_id, content)
VALUES (3, 5, 'Стефане, поздрави!');

-- Приемане на заявка за приятелство → тригерът записва лог
UPDATE friendships
SET status = 'accepted'
WHERE requester_id = 2 AND addressee_id = 5;

-- Проверка на логовете
SELECT * FROM communication_logs ORDER BY logged_at DESC LIMIT 5;

-- Проверка на статистиката
SELECT u.username, s.total_messages_sent, s.total_messages_received
FROM user_message_stats s
JOIN users u ON u.user_id = s.user_id
ORDER BY s.total_messages_sent DESC;
