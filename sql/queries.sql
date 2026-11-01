-- 1. Список всех напоминаний (SELECT)
SELECT id, event_id, remind_before, is_active FROM reminders ORDER BY id;

-- 2. Поиск активных напоминаний (WHERE)
SELECT * FROM reminders WHERE is_active = 1;

-- 3. Список событий с названиями категорий (JOIN)
SELECT events.title, events.event_date, categories.name AS category_name
FROM events
JOIN categories ON events.category_id = categories.id;

-- 4. Полная информация о напоминании (JOIN 3 таблиц)
SELECT 
    reminders.id,
    events.title AS event_title,
    events.event_date,
    users.name AS user_name,
    reminders.remind_before
FROM reminders
JOIN events ON reminders.event_id = events.id
JOIN users ON reminders.user_id = users.id
WHERE reminders.is_active = 1;

-- 5. Подсчёт общего количества активных напоминаний (COUNT)
SELECT COUNT(*) AS active_reminders FROM reminders WHERE is_active = 1;

-- 6. Статистика: сколько напоминаний у каждого пользователя (GROUP BY)
SELECT users.name, COUNT(reminders.id) AS reminders_count
FROM users
LEFT JOIN reminders ON users.id = reminders.user_id
GROUP BY users.id, users.name
ORDER BY reminders_count DESC;

-- 7. События без напоминаний (LEFT JOIN + IS NULL)
SELECT events.id, events.title 
FROM events
LEFT JOIN reminders ON events.id = reminders.event_id
WHERE reminders.id IS NULL;

-- 8. Список всех событий с сортировкой (Выборка списков)
SELECT id, title, event_date FROM events ORDER BY event_date DESC;

-- 9. Список всех пользователей по алфавиту (Выборка списков)
SELECT id, name, email FROM users ORDER BY name;

-- 10. Поиск конкретного напоминания по ID (Фильтрация WHERE)
SELECT * FROM reminders WHERE id = 1;

-- 11. Общее количество событий в базе (Агрегатные функции)
SELECT COUNT(*) AS total_events FROM events;

-- 12. Общее количество зарегистрированных пользователей (Агрегатные функции)
SELECT COUNT(*) AS total_users FROM users;