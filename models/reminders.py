"""Функции для работы с напоминаниями."""

from datetime import date


def days_until(event_date: str, today: date) -> int:
    """Вернуть количество дней от сегодня до события."""
    target = date.fromisoformat(event_date)
    return (target - today).days


def get_reminder(
    title: str, days_left: int, remind_before: int
) -> str:
    """Сформировать текст напоминания."""
    if days_left < 0:
        return f"Событие «{title}» прошло ({abs(days_left)} дн. назад)."
    if days_left == 0:
        return f"Сегодня — «{title}»!"
    if days_left <= remind_before:
        return f"Напоминание: до события «{title}» осталось {days_left} дн."
    return f"Событие «{title}» ещё не скоро (через {days_left} дн.)."


def get_booking_status(is_available: bool) -> str:
    """Текстовый статус"""
    if is_available:
        return "Событие можно запланировать"
    return "Событие уже наступило"


def add_reminder(
    reminders: list[dict], event_id: int, remind_before: int
) -> dict:
    """Создать напоминание для события."""
    new_id = max((r["id"] for r in reminders), default=0) + 1
    reminder = {
        "id": new_id,
        "event_id": event_id,
        "remind_before": remind_before,
    }
    reminders.append(reminder)
    return reminder


def cancel_reminder(reminders: list[dict], reminder_id: int) -> bool:
    """Отменить напоминание по идентификатору."""
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminders.remove(reminder)
            return True
    return False


def upcoming_events(
    events: dict[int, dict], today: date
) -> list[tuple[dict, int]]:
    """Вернуть список предстоящих событий с числом дней до каждого."""
    result = []
    for data in events.values():
        days = days_until(data["event_date"], today)
        if days >= 0:
            result.append((data, days))
    return sorted(result, key=lambda item: item[1])
