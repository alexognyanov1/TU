-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 3: Агрегатна функция и GROUP BY
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Заявка: За всеки потребител се извеждат броят на публикуваните
-- туити, общият брой харесвания, средната дължина на туита и
-- датата на последния туит.
-- Показват се само потребители с поне 1 туит, наредени по
-- общи харесвания в низходящ ред.
-- ------------------------------------------------------------
SELECT
    u.username,
    u.first_name,
    u.last_name,
    COUNT(DISTINCT t.id)     AS tweet_count,
    COUNT(DISTINCT l.user_id
          -- брои харесванията по двойка туит-потребител
         )                   AS total_likes,
    AVG(LENGTH(t.content))   AS avg_tweet_length,
    MAX(t.created_at)        AS last_tweet_date
FROM users u
JOIN  tweets t ON u.id = t.user_id AND t.is_deleted = 0
LEFT JOIN likes  l ON t.id = l.tweet_id
GROUP BY u.id, u.username, u.first_name, u.last_name
HAVING COUNT(DISTINCT t.id) > 0
ORDER BY total_likes DESC;
