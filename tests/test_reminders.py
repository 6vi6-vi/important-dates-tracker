from datetime import date

from models.reminders import (
    add_reminder,
    cancel_reminder,
    days_until,
    get_reminder,
)


def test_days_until():
    assert days_until("2026-10-05", date(2026, 9, 14)) == 21


def test_get_reminder_soon():
    assert "осталось 5 дн." in get_reminder("День рождения", 5, 7)


def test_add_reminder():
    reminders = []
    add_reminder(reminders, 1, 7)
    assert len(reminders) == 1


def test_cancel_reminder():
    reminders = []
    reminder = add_reminder(reminders, 1, 7)
    assert cancel_reminder(reminders, reminder["id"])
    assert not reminders
