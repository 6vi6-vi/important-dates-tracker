"""Сохранение и загрузка объектов проекта в JSON-файлах."""

import json
from typing import List

from models import Category, Event, Reminder, User
from models.events import find_events  # noqa: F401


def load_categories(filename: str) -> List[Category]:
    """Загрузить категории из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    return [
        Category(category_id=item["id"], name=item["name"]) for item in raw
    ]


def save_categories(filename: str, categories: List[Category]) -> None:
    """Сохранить категории в JSON-файл."""
    data = [{"id": c.id, "name": c.name} for c in categories]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    return [User.from_data(item) for item in raw]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    data = [
        {"id": u.id, "name": u.name, "email": u.email} for u in users
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def find_user_by_id(users: List[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_category_by_id(
    categories: List[Category], category_id: int
) -> Category | None:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category.id == category_id:
            return category
    return None


def find_event_by_id(events: List[Event], event_id: int) -> Event | None:
    """Найти событие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def load_events(
    filename: str,
    categories: List[Category],
    users: List[User],
) -> List[Event]:
    """Загрузить события из JSON и восстановить связи."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    events: List[Event] = []
    for item in raw:
        category = find_category_by_id(categories, item["category_id"])
        user = find_user_by_id(users, item["user_id"])
        if category is None or user is None:
            continue
        events.append(
            Event(
                event_id=item["id"],
                title=item["title"],
                event_date=item["event_date"],
                category=category,
                user=user,
                is_recurring=item["is_recurring"],
            )
        )
    return events


def save_events(filename: str, events: List[Event]) -> None:
    """Сохранить события в JSON-файл."""
    data = [
        {
            "id": event.id,
            "title": event.title,
            "event_date": event.event_date,
            "category_id": event.category.id,
            "user_id": event.user.id,
            "is_recurring": event.is_recurring,
        }
        for event in events
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_reminders(
    filename: str,
    events: List[Event],
) -> List[Reminder]:
    """Загрузить напоминания и восстановить связи с событиями."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    reminders: List[Reminder] = []
    for item in raw:
        event = find_event_by_id(events, item["event_id"])
        if event is None:
            continue
        reminders.append(
            Reminder(
                reminder_id=item["id"],
                event=event,
                remind_before=item["remind_before"],
                is_sent=item.get("is_sent", False),
            )
        )
    return reminders


def save_reminders(filename: str, reminders: List[Reminder]) -> None:
    """Сохранить напоминания в JSON-файл."""
    data = [
        {
            "id": reminder.id,
            "event_id": reminder.event.id,
            "remind_before": reminder.remind_before,
            "is_sent": reminder.is_sent,
        }
        for reminder in reminders
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
