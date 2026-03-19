-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 8: Тригер
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Тригер: after_tweet_soft_delete
--
-- Активира се СЛЕД UPDATE на таблица tweets.
-- Когато туит бъде "меко изтрит" (is_deleted: 0 -> 1),
-- тригерът автоматично:
--   1. Записва одит запис в tweet_deletion_log.
--   2. Намалява брояча tweet_count в user_stats с 1.
--
-- По този начин системата пази история на изтритите туити
-- и поддържа статистиките на потребителите синхронизирани.
-- ------------------------------------------------------------

DELIMITER $$

CREATE TRIGGER after_tweet_soft_delete
AFTER UPDATE ON tweets
FOR EACH ROW
BEGIN
    -- Проверяваме дали туитът току-що е бил изтрит (soft delete)
    IF NEW.is_deleted = 1 AND OLD.is_deleted = 0 THEN

        -- 1. Записваме одит лог
        INSERT INTO tweet_deletion_log (tweet_id, user_id, content, deleted_at)
        VALUES (OLD.id, OLD.user_id, OLD.content, NOW());

        -- 2. Обновяваме статистиката на потребителя
        UPDATE user_stats
        SET tweet_count = GREATEST(tweet_count - 1, 0)
        WHERE user_id = OLD.user_id;

    END IF;
END$$

DELIMITER ;

-- ------------------------------------------------------------
-- Демонстрация на тригера
-- ------------------------------------------------------------

-- Инициализираме статистиката преди теста
CALL update_all_user_stats();   -- (изпълнете след 10_procedure_cursor.sql)

-- Показваме tweet_count на потребител 1 преди изтриването
SELECT user_id, tweet_count
FROM user_stats
WHERE user_id = 1;

-- Меко изтриване на туит с id = 9 (автор: потребител 1)
UPDATE tweets SET is_deleted = 1 WHERE id = 9;

-- Проверяваме одит лога
SELECT * FROM tweet_deletion_log;

-- Проверяваме дали tweet_count е намалял
SELECT user_id, tweet_count
FROM user_stats
WHERE user_id = 1;
