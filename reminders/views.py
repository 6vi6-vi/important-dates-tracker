from datetime import date
from django.shortcuts import render

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


def _load_all():
    """Загрузить напоминания и события средствами ПР3."""
    categories = load_categories("data/categories.json")
    users = load_users("data/users.json")
    events = load_events("data/events.json", categories, users)
    reminders = load_reminders("data/reminders.json", events, users)
    return reminders, events


def reminders(request):
    reminders_list, _ = _load_all()
    reminders_list = sort_reminders_by_date(reminders_list)
    current_date = date.today()
    reminders_data = []
    for reminder in reminders_list:
        days = reminder.days_left(current_date)
        is_past = days < 0
        reminders_data.append({
            "obj": reminder,
            "days_left": days,
            "is_due": reminder.is_due(current_date),
            "is_past": is_past,
        })
    context = {
        "reminders": reminders_data,
    }
    return render(request, "reminders/reminder_list.html", context)


def reminder_detail(request, reminder_id):
    reminders_list, _ = _load_all()
    reminder = find_reminder_by_id(reminders_list, reminder_id)
    today = date.today()
    days_left = reminder.days_left(today) if reminder else 0
    context = {
        "reminder": reminder,
        "days_left": days_left,
        "is_past": days_left < 0 if reminder else False,
        "is_due": reminder.is_due(today) if reminder else False,
    }
    return render(
        request,
        "reminders/reminder_detail.html",
        context,
        status=404 if reminder is None else 200,
    )
