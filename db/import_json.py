import json
from db.database import get_connection


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def main():
    conn = get_connection()
    try:
        # Импорт пользователей
        users = load_json("data/users.json")
        conn.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
            [(u["id"], u["name"], u["email"]) for u in users],
        )
        # Импорт категорий
        categories = load_json("data/categories.json")
        conn.executemany(
            "INSERT INTO categories (id, name) VALUES (?, ?)",
            [(c["id"], c["name"]) for c in categories],
        )

        # Импорт событий
        events = load_json("data/events.json")
        conn.executemany(
            """INSERT INTO events (id, title, event_date, category_id, user_id, is_recurring)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [(e["id"], e["title"], e["event_date"], e["category_id"], e["user_id"],
              int(e["is_recurring"])) for e in events],
        )

        # Импорт напоминаний
        reminders = load_json("data/reminders.json")
        conn.executemany(
            """INSERT INTO reminders (id, event_id, user_id, remind_before, is_sent, is_active)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [(r["id"], r["event_id"], r["user_id"], r["remind_before"], int(r["is_sent"]),
              int(r["is_active"])) for r in reminders],
        )
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
