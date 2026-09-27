from datetime import date

from models import Category, Event, User
from models.events import (
    add_event,
    delete_event,
    filter_events_by_category,
    find_events,
    sort_events_by_date,
)


def make_user() -> User:
    return User(1, "Иван Петров", "ivan@example.com")


def make_category() -> Category:
    return Category(1, "Праздник")


def test_event_creation():
    event = Event(
        1,
        "День рождения",
        "2026-10-05",
        make_category(),
        make_user(),
        True,
    )
    assert event.id == 1
    assert event.title == "День рождения"
    assert event.is_recurring


def test_event_days_until():
    event = Event(
        1,
        "День рождения",
        "2026-10-05",
        make_category(),
        make_user(),
    )
    assert event.days_until(date(2026, 9, 14)) == 21


def test_event_matches():
    event = Event(
        1,
        "День рождения друга",
        "2026-10-05",
        make_category(),
        make_user(),
    )
    assert event.matches("друга")


def test_add_event():
    events = []
    event = add_event(
        events,
        "День рождения",
        "2026-10-05",
        make_category(),
        make_user(),
        True,
    )
    assert event is not None
    assert len(events) == 1


def test_add_event_empty_title():
    events = []
    event = add_event(
        events, "   ", "2026-10-05", make_category(), make_user()
    )
    assert event is None
    assert not events


def test_find_events():
    events = []
    add_event(
        events,
        "День рождения друга",
        "2026-10-05",
        make_category(),
        make_user(),
    )
    assert find_events(events, "друга")


def test_filter_events_by_category():
    events = []
    family = Category(1, "Семья")
    work = Category(2, "Работа")
    add_event(events, "Годовщина", "2026-12-20", family, make_user())
    add_event(events, "Дедлайн", "2026-11-01", work, make_user())
    assert len(filter_events_by_category(events, family)) == 1


def test_sort_events_by_date():
    events = []
    category = make_category()
    user = make_user()
    add_event(events, "Позже", "2026-12-20", category, user)
    add_event(events, "Раньше", "2026-10-05", category, user)
    ordered = sort_events_by_date(events)
    assert ordered[0].title == "Раньше"


def test_delete_event():
    events = []
    event = add_event(
        events, "Праздник", "2026-10-05", make_category(), make_user()
    )
    assert event is not None
    assert delete_event(events, event.id)
    assert not events
