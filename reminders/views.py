from datetime import date
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from events.models import Event
from reminders.models import Reminder
from users.models import User


def reminders(request):
    filter_type = request.GET.get("filter", "all")
    queryset = Reminder.objects.select_related("event", "user")
    today = date.today()
    if filter_type == "active":
        queryset = queryset.filter(is_active=True, event__event_date__gte=today)
    elif filter_type == "past":
        queryset = queryset.filter(event__event_date__lt=today).order_by("-event__event_date")
    elif filter_type == "inactive":
        queryset = queryset.filter(is_active=False)      
    if filter_type not in ["past"]:
        queryset = queryset.order_by("event__event_date")

    for reminder in queryset:
        days_left = (reminder.event.event_date - today).days
        reminder.is_past = days_left < 0
        reminder.days_left = days_left
        reminder.is_due = 0 <= days_left <= reminder.remind_before and reminder.is_active and not reminder.is_sent

    return render(request, "reminders/reminder_list.html", {
        "reminders": queryset,
        "filter_type": filter_type
    })


def reminder_detail(request, reminder_id):
    reminder = get_object_or_404(Reminder.objects.select_related("event", "user"), pk=reminder_id)
    today = date.today()
    days_left = (reminder.event.event_date - today).days
    return render(request, "reminders/reminder_detail.html", {
        "reminder": reminder,
        "days_left": days_left,
        "is_past": days_left < 0,
        "is_due": 0 <= days_left <= reminder.remind_before and reminder.is_active and not reminder.is_sent,
    })


def statistics(request):
    stats = User.objects.annotate(
        reminders_count=Count('reminders')
    ).order_by("-reminders_count")  
    active_count = Reminder.objects.filter(is_active=True).count()

    return render(request, "reminders/statistics.html", {
        "statistics": stats,
        "active_count": active_count
    })
