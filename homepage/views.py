import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def index(request):
    """Главная страница с общей статистикой из БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    total_events = conn.execute("SELECT COUNT(*) AS cnt FROM events").fetchone()["cnt"]
    total_reminders = conn.execute("SELECT COUNT(*) AS cnt FROM reminders").fetchone()["cnt"]
    conn.close()

    context = {
        "total_events": total_events,
        "total_reminders": total_reminders,
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    """Собственная страница 404."""
    return render(request, "404.html", status=404)
