import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def index(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    total_events = conn.execute("SELECT COUNT(*) AS cnt FROM events").fetchone()["cnt"]  # Запрос 11
    total_reminders = conn.execute("SELECT COUNT(*) AS cnt FROM reminders").fetchone()["cnt"]  # Запрос 12
    total_users = conn.execute("SELECT COUNT(*) AS cnt FROM users").fetchone()["cnt"]
    # Запрос 9: Список пользователей
    users = conn.execute("SELECT id, name, email FROM users ORDER BY name").fetchall()
    conn.close()

    return render(request, "homepage/index.html", {
        "total_events": total_events,
        "total_reminders": total_reminders,
        "total_users": total_users,
        "users": users,
    })


def page_not_found(request, exception):
    """Собственная страница 404."""
    return render(request, "404.html", status=404)
