-- ============================================================
-- ТЕМА №12 – Система за комуникация между потребители
-- Задача 9: Процедура с курсор
-- ============================================================
-- Процедурата обхожда всички потребители чрез курсор и за
-- всеки синхронизира таблицата user_message_stats с реалния
-- брой изпратени и получени съобщения от таблица messages.
-- Накрая извежда обобщен отчет.
-- ============================================================

USE messaging_system;

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_sync_message_stats$$

CREATE PROCEDURE sp_sync_message_stats()
BEGIN
    -- Променливи за курсора
    DECLARE v_user_id       INT;
    DECLARE v_sent_count    INT;
    DECLARE v_recv_count    INT;
    DECLARE v_done          TINYINT DEFAULT 0;

    -- Курсор върху всички потребители
    DECLARE cur_users CURSOR FOR
        SELECT user_id FROM users WHERE is_active = 1;

    -- Handler за края на курсора
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    OPEN cur_users;

    user_loop: LOOP
        FETCH cur_users INTO v_user_id;

        IF v_done THEN
            LEAVE user_loop;
        END IF;

        -- Изчисли реалния брой изпратени съобщения
        SELECT COUNT(*) INTO v_sent_count
        FROM messages
        WHERE sender_id = v_user_id;

        -- Изчисли реалния брой получени съобщения
        SELECT COUNT(*) INTO v_recv_count
        FROM messages
        WHERE receiver_id = v_user_id;

        -- Актуализирай или вмъкни запис в user_message_stats
        INSERT INTO user_message_stats
            (user_id, total_messages_sent, total_messages_received)
        VALUES
            (v_user_id, v_sent_count, v_recv_count)
        ON DUPLICATE KEY UPDATE
            total_messages_sent     = v_sent_count,
            total_messages_received = v_recv_count,
            last_updated            = NOW();

    END LOOP;

    CLOSE cur_users;

    -- Отчет след синхронизацията
    SELECT
        u.user_id,
        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
        u.username,
        s.total_messages_sent,
        s.total_messages_received,
        (s.total_messages_sent + s.total_messages_received) AS total_activity,
        s.last_updated
    FROM user_message_stats s
    JOIN users u ON u.user_id = s.user_id
    ORDER BY total_activity DESC;
END$$

DELIMITER ;

-- -----------------------------------------------------------
-- Изпълнение на процедурата
-- -----------------------------------------------------------
CALL sp_sync_message_stats();
