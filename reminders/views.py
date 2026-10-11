"""Views приложения reminders: список и карточка напоминаний."""

from datetime import date

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models import Reminder  # noqa: F401  (тип для аннотаций)
from models.reminders import (
    find_reminder_by_id,
    sort_reminders_by_date,
)
from storage import (
    load_categories,
    load_events,
    load_reminders,
    load_users,
)


def _load_all() -> tuple[list, list]:
    """Загрузить напоминания и события средствами ПР3."""
    categories = load_categories("data/categories.json")
    users = load_users("data/users.json")
    events = load_events("data/events.json", categories, users)
    reminders = load_reminders("data/reminders.json", events, users)
    return reminders, events


def reminders(request: HttpRequest) -> HttpResponse:
    """Страница /reminders/: список напоминаний."""
    reminders_list, _ = _load_all()
    reminders_list = sort_reminders_by_date(reminders_list)

    if not reminders_list:
        content = '<p class="text-muted">Напоминаний нет.</p>'
        return HttpResponse(page("Напоминания", content))

    items = ""
    today = date.today()
    for reminder in reminders_list:
        days_left = reminder.days_left(today)
        state = "активно" if reminder.is_active else "отменено"
        badge = "bg-success" if reminder.is_active else "bg-secondary"
        items += f"""
        <a href="/reminders/{reminder.id}/"
           class="list-group-item list-group-item-action">
            <div class="d-flex justify-content-between">
                <span>
                    {reminder.event.title}
                    для {reminder.user.name}
                </span>
                <span class="badge {badge}">{state}</span>
            </div>
            <small class="text-muted">
                за {reminder.remind_before} дн.
                (осталось {days_left} дн.)
            </small>
        </a>
        """
    content = f'<div class="list-group">{items}</div>'
    return HttpResponse(page("Напоминания", content))


def reminder_detail(
    request: HttpRequest, reminder_id: int
) -> HttpResponse:
    """Страница /reminders/<int:reminder_id>/."""
    reminders_list, _ = _load_all()
    reminder = find_reminder_by_id(reminders_list, reminder_id)

    if reminder is None:
        content = """
        <p class="text-danger">Напоминание не найдено.</p>
        <a href="/reminders/"
           class="btn btn-outline-secondary">
            ← к списку напоминаний
        </a>
        """
        return HttpResponse(
            page("Напоминание не найдено", content), status=404
        )

    today = date.today()
    days_left = reminder.days_left(today)
    is_due = reminder.is_due(today)
    state = "активно" if reminder.is_active else "отменено"
    if reminder.is_sent:
        state = "показано"
    badge = "bg-success" if reminder.is_active else "bg-secondary"
    due_badge = (
        '<span class="badge bg-warning text-dark">пора показать</span>'
        if is_due
        else ""
    )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                Напоминание №{reminder.id}
            </h5>
            <p class="card-text">
                <strong>Событие:</strong> {reminder.event.title}
            </p>
            <p class="card-text">
                <strong>Дата события:</strong>
                {reminder.event.event_date}
            </p>
            <p class="card-text">
                <strong>Пользователь:</strong>
                {reminder.user.name} ({reminder.user.email})
            </p>
            <p class="card-text">
                <strong>Напомнить за:</strong>
                {reminder.remind_before} дн.
            </p>
            <p class="card-text">
                <strong>Осталось дней:</strong> {days_left}
            </p>
            <p class="card-text">
                <strong>Состояние:</strong>
                <span class="badge {badge}">{state}</span>
                {due_badge}
            </p>
            <a href="/reminders/"
               class="btn btn-outline-secondary">
                ← к списку напоминаний
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Напоминание №{reminder.id}", content), status=200
    )
