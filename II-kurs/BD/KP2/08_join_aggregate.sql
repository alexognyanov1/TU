-- ============================================================
-- КУРСОВ ПРОЕКТ - БАЗИ ОТ ДАННИ
-- Тема №13: Елементаризиран вариант на X (Twitter)
-- Задача 7: JOIN и агрегатна функция едновременно
-- ============================================================

USE twitter_db;

-- ------------------------------------------------------------
-- Заявка: Класация на туитите по популярност - за всеки туит
-- се показват авторът, съдържанието, броят харесвания и
-- броят ретуити, като всички се получават чрез JOIN-ове
-- и се агрегират с COUNT.
-- ------------------------------------------------------------
SELECT
    u.username,
    u.first_name,
    u.last_name,
    t.content,
    t.created_at,
    COUNT(DISTINCT l.user_id) AS likes_count,
    COUNT(DISTINCT r.user_id) AS retweets_count,
    COUNT(DISTINCT l.user_id) + COUNT(DISTINCT r.user_id) AS engagement_score
FROM tweets t
INNER JOIN users    u ON t.user_id   = u.id
LEFT  JOIN likes    l ON t.id        = l.tweet_id
LEFT  JOIN retweets r ON t.id        = r.tweet_id
WHERE t.is_deleted = 0
GROUP BY
    t.id,
    u.username,
    u.first_name,
    u.last_name,
    t.content,
    t.created_at
ORDER BY engagement_score DESC, t.created_at DESC;
