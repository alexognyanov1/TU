-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 9: Процедура с курсор
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Процедура: update_all_user_stats
--
-- Обхожда с курсор всички активни потребители един по един
-- и за всеки изчислява и записва в user_stats:
--   - tweet_count     : брой публикувани (неизтрити) туити
--   - follower_count  : брой потребители, следящи профила
--   - following_count : брой профили, следени от потребителя
--
-- INSERT ... ON DUPLICATE KEY UPDATE гарантира, че записът
-- се създава при нужда или се обновява ако вече съществува.
-- ------------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE update_all_user_stats()
BEGIN
    -- Променливи за курсора
    DECLARE v_done            INT DEFAULT FALSE;
    DECLARE v_user_id         INT;
    DECLARE v_tweet_count     INT;
    DECLARE v_follower_count  INT;
    DECLARE v_following_count INT;

    -- Курсор, обхождащ всички активни потребители
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users WHERE is_active = 1;

    -- Handler за края на резултатния набор
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

    OPEN user_cursor;

    process_loop: LOOP
        FETCH user_cursor INTO v_user_id;

        IF v_done THEN
            LEAVE process_loop;
        END IF;

        -- Брой активни туити
        SELECT COUNT(*)
        INTO   v_tweet_count
        FROM   tweets
        WHERE  user_id    = v_user_id
          AND  is_deleted = 0;

        -- Брой последователи (хора, следящи v_user_id)
        SELECT COUNT(*)
        INTO   v_follower_count
        FROM   follows
        WHERE  followed_id = v_user_id;

        -- Брой следвани (хора, следени от v_user_id)
        SELECT COUNT(*)
        INTO   v_following_count
        FROM   follows
        WHERE  follower_id = v_user_id;

        -- Запис/обновяване на статистиката
        INSERT INTO user_stats (user_id, tweet_count, follower_count, following_count)
        VALUES (v_user_id, v_tweet_count, v_follower_count, v_following_count)
        ON DUPLICATE KEY UPDATE
            tweet_count     = v_tweet_count,
            follower_count  = v_follower_count,
            following_count = v_following_count;

    END LOOP process_loop;

    CLOSE user_cursor;

    SELECT 'Статистиката на всички потребители е обновена успешно.' AS result;
END$$

DELIMITER ;

-- ------------------------------------------------------------
-- Извикване на процедурата
-- ------------------------------------------------------------
CALL update_all_user_stats();

-- ------------------------------------------------------------
-- Преглед на резултатите
-- ------------------------------------------------------------
SELECT
    u.username,
    u.first_name,
    u.last_name,
    us.tweet_count,
    us.follower_count,
    us.following_count
FROM users u
JOIN user_stats us ON u.id = us.user_id
ORDER BY us.follower_count DESC;
