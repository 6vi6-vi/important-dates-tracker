"""Функции для работы с событиями."""

from datetime import date


def add_event(
    events: dict[int, dict],
    title: str,
    event_date: date,
    category: str,
    is_recurring: bool,
) -> int:
    """Добавить событие в словарь events.
    Возвращает идентификатор созданного события.
    """
    new_id = max(events.keys(), default=0) + 1
    events[new_id] = {
        "title": title.strip(),
        "event_date": event_date.isoformat(),
        "category": category.strip(),
        "is_recurring": bool(is_recurring),
    }
    return new_id


def find_events(events: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти события по подстроке названия."""
    query_lower = query.lower()
    return {
        event_id: data
        for event_id, data in events.items()
        if query_lower in data["title"].lower()
    }


def filter_events_by_category(
    events: dict[int, dict], category: str
) -> dict[int, dict]:
    """Отобрать события по категории."""
    category_lower = category.lower()
    return {
        event_id: data
        for event_id, data in events.items()
        if data["category"].lower() == category_lower
    }


def sort_events_by_date(events: dict[int, dict]) -> list[dict]:
    """Отсортировать события по дате."""
    return sorted(events.values(), key=lambda item: item["event_date"])


def delete_event(events: dict[int, dict], event_id: int) -> bool:
    """Удалить событие по идентификатору."""
    if event_id in events:
        del events[event_id]
        return True
    return False
