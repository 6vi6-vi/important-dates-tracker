from django.shortcuts import render
from events.models import Event
from reminders.models import Reminder
from users.models import User


def index(request):
    total_events = Event.objects.count()
    total_reminders = Reminder.objects.count()
    total_users = User.objects.count()
    users = User.objects.all()

    return render(request, "homepage/index.html", {
        "total_events": total_events,
        "total_reminders": total_reminders,
        "total_users": total_users,
        "users": users,
    })


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
