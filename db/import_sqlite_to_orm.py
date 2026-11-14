import os
import sys
import sqlite3
from datetime import date
from pathlib import Path
import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from users.models import User
from events.models import Category, Event
from reminders.models import Reminder

SOURCE_DB = BASE_DIR / "data" / "important_dates.sqlite"


def main():
    if not SOURCE_DB.exists():
        print(f"Файл базы не найден: {SOURCE_DB}")
        return

    print("Подключение к старой базе...")
    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row     
        users = conn.execute("SELECT * FROM users").fetchall()
        categories = conn.execute("SELECT * FROM categories").fetchall()
        events = conn.execute("SELECT * FROM events").fetchall()
        reminders = conn.execute("SELECT * FROM reminders").fetchall()

    print("Начинаем перенос данных в Django ORM...")
    with transaction.atomic():
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"], "email": row["email"]},
            )
        for row in categories:
            Category.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )
        for row in events:
            Event.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "title": row["title"],
                    "event_date": date.fromisoformat(row["event_date"]),
                    "category_id": row["category_id"],
                    "user_id": row["user_id"],
                    "is_recurring": bool(row["is_recurring"]),
                },
            )
        for row in reminders:
            Reminder.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "event_id": row["event_id"],
                    "user_id": row["user_id"],
                    "remind_before": row["remind_before"],
                    "is_sent": bool(row["is_sent"]),
                    "is_active": bool(row["is_active"]),
                },
            )         
    print("Данные успешно перенесены в Django ORM!")


if __name__ == "__main__":
    main()
