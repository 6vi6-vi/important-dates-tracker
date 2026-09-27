from datetime import date

from models import Category, Event, User
from models.reminders import (
    add_reminder,
    cancel_reminder,
    get_reminder,
    upcoming_events,
)


def make_event() -> Event:
    return Event(
        1,
        "День рождения",
        "2026-10-05",
        Category(1, "Праздник"),
        User(1, "Иван", "ivan@example.com"),
    )


def test_reminder_creation():
    event = make_event()
    reminders = []
    reminder = add_reminder(reminders, event, 7)
    assert reminder.id == 1
    assert reminder.event is event
    assert len(reminders) == 1


def test_reminder_is_due():
    event = make_event()
    reminders = []
    reminder = add_reminder(reminders, event, 7)
    assert reminder.is_due(5)
    assert not reminder.is_due(10)


def test_reminder_cancel():
    reminders = []
    reminder = add_reminder(reminders, make_event(), 7)
    assert cancel_reminder(reminders, reminder.id)
    assert not reminders


def test_get_reminder_soon():
    assert "осталось 5 дн." in get_reminder("День рождения", 5, 7)


def test_upcoming_events():
    event = make_event()
    upcoming = upcoming_events([event], date(2026, 9, 14))
    assert len(upcoming) == 1
    assert upcoming[0][1] == 21
