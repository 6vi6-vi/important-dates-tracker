from django.db.models import Count
from events.models import Event, Category
from reminders.models import Reminder
from users.models import User
from django.shortcuts import render


def index(request):
    total_events = Event.objects.count()
    total_reminders = Reminder.objects.count()
    users = User.objects.all()
    categories_stats = Category.objects.annotate(events_count=Count('events'))

    return render(request, "homepage/index.html", {
        "total_events": total_events,
        "total_reminders": total_reminders,
        "users": users,
        "categories_stats": categories_stats,
    })


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
