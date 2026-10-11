from datetime import date

from models import Category, Event, User
from models.reminders import (
    add_reminder,
    cancel_reminder,
    filter_active_reminders,
    find_reminder_by_id,
    get_due_reminders,
    sort_reminders_by_date,
)


def make_event(event_date: str = "2026-10-05") -> Event:
    return Event(
        1,
        "День рождения",
        event_date,
        Category(1, "Праздник"),
        User(1, "Иван", "ivan@example.com"),
    )


def make_user() -> User:
    return User(1, "Иван", "ivan@example.com")


def test_reminder_creation():
    reminders = []
    reminder = add_reminder(reminders, make_event(), make_user(), 7)
    assert reminder is not None
    assert reminder.id == 1
    assert reminder.is_active
    assert not reminder.is_sent


def test_reminder_is_due():
    reminders = []
    reminder = add_reminder(reminders, make_event(), make_user(), 7)
    assert reminder.is_due(date(2026, 9, 30))
    assert not reminder.is_due(date(2026, 9, 20))


def test_reminder_cancel():
    reminders = []
    reminder = add_reminder(reminders, make_event(), make_user(), 7)
    assert cancel_reminder(reminders, reminder.id)
    assert not reminder.is_active
    assert not filter_active_reminders(reminders)


def test_reminder_mark_sent():
    reminders = []
    reminder = add_reminder(reminders, make_event(), make_user(), 7)
    reminder.mark_sent()
    assert reminder.is_sent
    assert not reminder.is_due(date(2026, 9, 30))


def test_sort_reminders_by_date():
    reminders = []
    add_reminder(
        reminders, make_event("2026-12-20"), make_user(), 7
    )
    add_reminder(
        reminders, make_event("2026-10-05"), make_user(), 7
    )
    ordered = sort_reminders_by_date(reminders)
    assert ordered[0].event.event_date == "2026-10-05"


def test_find_reminder_by_id():
    reminders = []
    reminder = add_reminder(reminders, make_event(), make_user(), 7)
    assert find_reminder_by_id(reminders, reminder.id) is reminder
    assert find_reminder_by_id(reminders, 999) is None


def test_get_due_reminders():
    reminders = []
    add_reminder(reminders, make_event("2026-10-05"), make_user(), 7)
    assert get_due_reminders(reminders, date(2026, 10, 1))
    assert not get_due_reminders(reminders, date(2026, 9, 1))
