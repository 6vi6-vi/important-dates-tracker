from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render
from reminders.models import Reminder
from users.models import User


def reminders(request):
    filter_type = request.GET.get("filter", "all")
    sort = request.GET.get("sort", "date")
    query = request.GET.get("q", "").strip()
    queryset = Reminder.objects.select_related("event", "user")
    today = date.today()

    if filter_type == "active":
        queryset = queryset.filter(
            status=Reminder.Status.ACTIVE,
            event__event_date__gte=today
        )
    elif filter_type == "past":
        queryset = queryset.filter(event__event_date__lt=today)
    elif filter_type == "inactive":
        queryset = queryset.filter(status=Reminder.Status.CANCELLED)

    if query:
        queryset = queryset.filter(
            Q(event__title__icontains=query) | Q(user__name__icontains=query)
        )

    if sort == "title":
        queryset = queryset.order_by("event__title")
    elif sort == "date_desc":
        queryset = queryset.order_by("-event__event_date")
    else:
        queryset = queryset.order_by("event__event_date")

    for reminder in queryset:
        days_left = (reminder.event.event_date - today).days
        reminder.is_past = days_left < 0
        reminder.days_left = days_left
        reminder.is_due = (
            0 <= days_left <= reminder.remind_before
            and reminder.status == Reminder.Status.ACTIVE
            and not reminder.is_sent
        )

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "reminders/reminder_list.html", {
        "reminders": page_obj,
        "page_obj": page_obj,
        "filter_type": filter_type,
        "sort": sort,
        "search_query": query,
    })


def reminder_detail(request, reminder_id):
    reminder = get_object_or_404(Reminder.objects.select_related("event", "user"), pk=reminder_id)
    today = date.today()
    days_left = (reminder.event.event_date - today).days
    return render(request, "reminders/reminder_detail.html", {
        "reminder": reminder,
        "days_left": days_left,
        "is_past": days_left < 0,
        "is_due": (
            0 <= days_left <= reminder.remind_before
            and reminder.status == Reminder.Status.ACTIVE
            and not reminder.is_sent
        ),
    })


def statistics(request):
    stats = User.objects.annotate(
        reminders_count=Count('reminders')
    ).order_by("-reminders_count")
    active_count = Reminder.objects.filter(status=Reminder.Status.ACTIVE).count()

    return render(request, "reminders/statistics.html", {
        "statistics": stats,
        "active_count": active_count
    })
