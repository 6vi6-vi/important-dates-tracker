from datetime import date

from events import (
    add_event,
    delete_event,
    filter_events_by_category,
    find_events,
    sort_events_by_date,
)


def test_add_event():
    events = {}
    add_event(
        events, "День рождения", date(2026, 10, 5), "Праздник", True
    )
    assert len(events) == 1


def test_find_events():
    events = {}
    add_event(
        events, "День рождения друга", date(2026, 10, 5), "Праздник", True
    )
    assert find_events(events, "друга")


def test_filter_events_by_category():
    events = {}
    add_event(events, "Годовщина", date(2026, 12, 20), "Семья", True)
    add_event(events, "Дедлайн", date(2026, 11, 1), "Работа", False)
    assert len(filter_events_by_category(events, "Семья")) == 1


def test_sort_events_by_date():
    events = {}
    add_event(events, "Праздник2", date(2026, 12, 20), "Семья", True)
    add_event(events, "Праздник1", date(2026, 10, 5), "Работа", False)
    ordered = sort_events_by_date(events)
    assert ordered[0]["title"] == "Праздник1"


def test_delete_event():
    events = {}
    new_id = add_event(
        events, "Праздник", date(2026, 10, 5), "Семья", True
    )
    assert delete_event(events, new_id)
    assert not events
