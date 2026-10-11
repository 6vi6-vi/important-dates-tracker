"""Класс напоминания и функции работы с напоминаниями."""

from datetime import date
from typing import List, Optional

from .events import Event
from .users import User


class Reminder:
    """Напоминание — главная сущность сервиса."""

    def __init__(
        self,
        reminder_id: int,
        event: Event,
        user: User,
        remind_before: int,
        is_sent: bool = False,
        is_active: bool = True,
    ) -> None:
        """Создать объект напоминания."""
        self.id = reminder_id
        self.event = event
        self.user = user
        self.remind_before = remind_before
        self.is_sent = is_sent
        self.is_active = is_active

    def days_left(self, today: date) -> int:
        """Сколько дней осталось до события."""
        return self.event.days_until(today)

    def is_due(self, today: date) -> bool:
        """Пора ли показать напоминание."""
        if not self.is_active or self.is_sent:
            return False
        return 0 <= self.days_left(today) <= self.remind_before

    def cancel(self) -> None:
        """Отменить напоминание."""
        self.is_active = False

    def mark_sent(self) -> None:
        """Отметить напоминание как отправленное."""
        self.is_sent = True

    def matches(self, query: str) -> bool:
        """Проверить совпадение с запросом по названию события."""
        return self.event.matches(query)

    @staticmethod
    def validate_remind_before(value: int) -> bool:
        """Проверить корректность срока напоминания."""
        return value >= 0

    @classmethod
    def from_data(
        cls, data: dict, events: List[Event], users: List[User]
    ) -> Optional["Reminder"]:
        """Создать напоминание из данных JSON."""
        event = next(
            (e for e in events if e.id == data["event_id"]), None
        )
        user = next(
            (u for u in users if u.id == data["user_id"]), None
        )
        if event is None or user is None:
            return None
        return cls(
            reminder_id=data["id"],
            event=event,
            user=user,
            remind_before=data["remind_before"],
            is_sent=data.get("is_sent", False),
            is_active=data.get("is_active", True),
        )

    def __str__(self) -> str:
        state = "активно" if self.is_active else "отменено"
        if self.is_sent:
            state = "показано"
        return (
            f"[{self.id}] {self.event.title} для {self.user.name} — "
            f"за {self.remind_before} дн. ({state})"
        )


def add_reminder(
    reminders: List[Reminder],
    event: Event,
    user: User,
    remind_before: int,
) -> Optional[Reminder]:
    """Создать объект Reminder и добавить его в коллекцию."""
    if not Reminder.validate_remind_before(remind_before):
        return None
    new_id = max((r.id for r in reminders), default=0) + 1
    reminder = Reminder(new_id, event, user, remind_before)
    reminders.append(reminder)
    return reminder


def find_reminders(
    reminders: List[Reminder], query: str
) -> List[Reminder]:
    """Найти напоминания по подстроке в названии события."""
    return [r for r in reminders if r.matches(query)]


def find_reminder_by_id(
    reminders: List[Reminder], reminder_id: int
) -> Optional[Reminder]:
    """Найти напоминание по идентификатору."""
    for reminder in reminders:
        if reminder.id == reminder_id:
            return reminder
    return None


def filter_active_reminders(
    reminders: List[Reminder],
) -> List[Reminder]:
    """Отобрать только активные напоминания."""
    return [r for r in reminders if r.is_active]


def filter_reminders_by_user(
    reminders: List[Reminder], user: User
) -> List[Reminder]:
    """Отобрать напоминания конкретного пользователя."""
    return [r for r in reminders if r.user is user]


def get_due_reminders(
    reminders: List[Reminder], today: date
) -> List[Reminder]:
    """Вернуть напоминания, которые пора показать."""
    return [r for r in reminders if r.is_due(today)]


def sort_reminders_by_date(
    reminders: List[Reminder],
) -> List[Reminder]:
    """Отсортировать напоминания по дате события."""
    return sorted(reminders, key=lambda r: r.event.event_date)


def cancel_reminder(
    reminders: List[Reminder], reminder_id: int
) -> bool:
    """Отменить напоминание по идентификатору."""
    reminder = find_reminder_by_id(reminders, reminder_id)
    if reminder is None:
        return False
    reminder.cancel()
    return True


def show_reminders(reminders: List[Reminder]) -> None:
    """Вывести список напоминаний (консольная версия)."""
    if not reminders:
        print("Список напоминаний пуст.")
        return
    for reminder in reminders:
        print(reminder)
