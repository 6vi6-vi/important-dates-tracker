"""Класс напоминания и функции работы с напоминаниями."""

from datetime import date
from typing import List, Optional, Tuple

from .events import Event


class Reminder:
    """Напоминание о событии."""

    def __init__(
        self,
        reminder_id: int,
        event: Event,
        remind_before: int,
        is_sent: bool = False,
    ) -> None:
        """Создать объект напоминания."""
        self.id = reminder_id
        self.event = event
        self.remind_before = remind_before
        self.is_sent = is_sent

    def is_due(self, days_left: int) -> bool:
        """Проверить, пора ли показать напоминание."""
        return 0 <= days_left <= self.remind_before

    def mark_sent(self) -> None:
        """Отметить напоминание как показанное."""
        self.is_sent = True

    def __str__(self) -> str:
        state = "показано" if self.is_sent else "активно"
        return (
            f"[{self.id}] {self.event.title} — "
            f"за {self.remind_before} дн. ({state})"
        )


def add_reminder(
    reminders: List[Reminder], event: Event, remind_before: int
) -> Reminder:
    """Создать напоминание для события."""
    new_id = max((r.id for r in reminders), default=0) + 1
    reminder = Reminder(
        reminder_id=new_id,
        event=event,
        remind_before=remind_before,
    )
    reminders.append(reminder)
    return reminder


def cancel_reminder(reminders: List[Reminder], reminder_id: int) -> bool:
    """Удалить напоминание по идентификатору."""
    for reminder in reminders:
        if reminder.id == reminder_id:
            reminders.remove(reminder)
            return True
    return False


def get_reminder(title: str, days_left: int, remind_before: int) -> str:
    """Сформировать текст напоминания."""
    if days_left < 0:
        return f"Событие «{title}» прошло ({abs(days_left)} дн. назад)."
    if days_left == 0:
        return f"Сегодня — «{title}»!"
    if days_left <= remind_before:
        return f"Напоминание: до события «{title}» осталось {days_left} дн."
    return f"Событие «{title}» ещё не скоро (через {days_left} дн.)."


def get_booking_status(is_available: bool) -> str:
    """Текстовый статус."""
    if is_available:
        return "Событие можно запланировать"
    return "Событие уже наступило"


def upcoming_events(
    events: List[Event], today: date
) -> List[Tuple[Event, int]]:
    """Вернуть предстоящие события с числом дней до каждого."""
    result: List[Tuple[Event, int]] = []
    for event in events:
        days = event.days_until(today)
        if days >= 0:
            result.append((event, days))
    return sorted(result, key=lambda item: item[1])


def show_reminders(reminders: List[Reminder]) -> None:
    """Вывести список напоминаний."""
    if not reminders:
        print("Список напоминаний пуст.")
        return
    for reminder in reminders:
        print(reminder)


def find_reminder_by_id(
    reminders: List[Reminder], reminder_id: int
) -> Optional[Reminder]:
    """Найти напоминание по идентификатору."""
    for reminder in reminders:
        if reminder.id == reminder_id:
            return reminder
    return None
