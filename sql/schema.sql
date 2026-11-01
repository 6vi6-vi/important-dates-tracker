CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_recurring INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    remind_before INTEGER NOT NULL,
    is_sent INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);