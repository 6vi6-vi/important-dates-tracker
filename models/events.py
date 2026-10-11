"""Класс события и функции работы с событиями."""

from datetime import date
from typing import List, Optional

from .categories import Category
from .users import User


class Event:
    """Важное событие пользователя."""

    def __init__(
        self,
        event_id: int,
        title: str,
        event_date: str,
        category: Category,
        user: User,
        is_recurring: bool = False,
    ) -> None:
        """Создать объект события."""
        self.id = event_id
        self.title = title
        self.event_date = event_date
        self.category = category
        self.user = user
        self.is_recurring = is_recurring

    def days_until(self, today: date) -> int:
        """Вернуть количество дней до события."""
        target = date.fromisoformat(self.event_date)
        return (target - today).days

    def matches(self, query: str) -> bool:
        """Проверить совпадение названия с запросом."""
        return query.lower() in self.title.lower()

    @staticmethod
    def validate_title(title: str) -> bool:
        """Проверить корректность названия события."""
        return bool(title.strip())

    def __str__(self) -> str:
        kind = "ежегодное" if self.is_recurring else "одноразовое"
        return (
            f"[{self.id}] {self.title} — {self.event_date} "
            f"({self.category.name}, {kind}, {self.user.name})"
        )


def add_event(
    events: List[Event],
    title: str,
    event_date: str,
    category: Category,
    user: User,
    is_recurring: bool = False,
) -> Optional[Event]:
    """Создать объект Event и добавить его в коллекцию."""
    if not Event.validate_title(title):
        return None
    new_id = max((e.id for e in events), default=0) + 1
    event = Event(
        event_id=new_id,
        title=title.strip(),
        event_date=event_date,
        category=category,
        user=user,
        is_recurring=is_recurring,
    )
    events.append(event)
    return event


def find_events(events: List[Event], query: str) -> List[Event]:
    """Найти события по подстроке названия."""
    return [e for e in events if e.matches(query)]


def find_event_by_id(
    events: List[Event], event_id: int
) -> Optional[Event]:
    """Найти событие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def sort_events_by_date(events: List[Event]) -> List[Event]:
    """Отсортировать события по дате."""
    return sorted(events, key=lambda e: e.event_date)


def show_events(events: List[Event]) -> None:
    """Вывести список событий (консольная версия)."""
    if not events:
        print("Список событий пуст.")
        return
    for event in events:
        print(event)
