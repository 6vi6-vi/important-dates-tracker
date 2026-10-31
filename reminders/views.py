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
    """Страница /reminders/: список напоминаний."""
    reminders_list, _ = _load_all()
    reminders_list = sort_reminders_by_date(reminders_list)
    
    context = {
        "reminders": reminders_list,
        "today": date.today(),
    }
    return render(request, "reminders/reminder_list.html", context)


def reminder_detail(request, reminder_id):
    """Страница /reminders/<int:reminder_id>/."""
    reminders_list, _ = _load_all()
    reminder = find_reminder_by_id(reminders_list, reminder_id)
    
    context = {
        "reminder": reminder,
        "today": date.today(),
    }
    return render(
        request,
        "reminders/reminder_detail.html",
        context,
        status=404 if reminder is None else 200,
    )
