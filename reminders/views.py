from datetime import date
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from reminders.models import Reminder
from users.models import User
from .forms import ReminderFilterForm, ReminderForm
from django.views.decorators.http import require_POST


def reminders(request):
    form = ReminderFilterForm(request.GET or None)
    queryset = Reminder.objects.select_related("event", "user")
    today = date.today()

    sort = "date"
    filter_type = "all"

    if form.is_bound and form.is_valid():
        selected_event = form.cleaned_data.get("event")
        selected_user = form.cleaned_data.get("user")
        filter_type = form.cleaned_data.get("status") or "all"
        sort = form.cleaned_data.get("sort") or "date"

        if selected_event:
            queryset = queryset.filter(event=selected_event)
        if selected_user:
            queryset = queryset.filter(user=selected_user)

    if filter_type == "active":
        queryset = queryset.filter(status=Reminder.Status.ACTIVE, event__event_date__gte=today)
    elif filter_type == "past":
        queryset = queryset.filter(event__event_date__lt=today).exclude(status=Reminder.Status.CANCELLED)
    elif filter_type == "inactive":
        queryset = queryset.filter(status=Reminder.Status.CANCELLED)

    if sort == "title":
        queryset = queryset.order_by("event__title")
    else:
        queryset = queryset.order_by("event__event_date")

    for reminder in queryset:
        days_left = (reminder.event.event_date - today).days
        reminder.is_past = days_left < 0
        reminder.days_left = days_left
        reminder.is_due = (
            0 <= days_left <= reminder.remind_before
            and reminder.current_status == Reminder.Status.ACTIVE
            and not reminder.is_sent
        )

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "reminders/reminder_list.html", {
        "reminders": page_obj,
        "page_obj": page_obj,
        "form": form,
    })


def reminder_detail(request, slug):
    reminder = get_object_or_404(
        Reminder.objects.select_related("event", "user"),
        slug=slug
    )
    today = date.today()
    days_left = (reminder.event.event_date - today).days
    return render(request, "reminders/reminder_detail.html", {
        "reminder": reminder,
        "days_left": days_left,
        "is_past": days_left < 0,
        "is_due": (
            0 <= days_left <= reminder.remind_before
            and reminder.current_status == Reminder.Status.ACTIVE
            and not reminder.is_sent
        ),
    })


def reminder_create(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save()
            return redirect("reminders:detail", slug=reminder.slug)
    else:
        form = ReminderForm(initial={"remind_before": 7})
    return render(request, "reminders/reminder_form.html", {"form": form})


def reminder_update(request, slug):
    reminder = get_object_or_404(Reminder, slug=slug)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect("reminders:detail", slug=reminder.slug)
    else:
        form = ReminderForm(instance=reminder)
    return render(request, "reminders/reminder_form.html", {"form": form, "reminder": reminder})


@require_POST
def reminder_cancel(request, slug):
    reminder = get_object_or_404(Reminder.objects.filter(status=Reminder.Status.ACTIVE), slug=slug)
    reminder.status = Reminder.Status.CANCELLED
    reminder.save()
    return redirect("reminders:list")


def statistics(request):
    stats = User.objects.annotate(
        reminders_count=Count('reminders')
    ).order_by("-reminders_count")
    today = date.today()
    active_count = Reminder.objects.filter(
        status=Reminder.Status.ACTIVE,
        event__event_date__gte=today
    ).count()

    completed_count = Reminder.objects.filter(
        event__event_date__lt=today
    ).exclude(status=Reminder.Status.CANCELLED).count()

    cancelled_count = Reminder.objects.filter(
        status=Reminder.Status.CANCELLED
    ).count()

    return render(request, "reminders/statistics.html", {
        "statistics": stats,
        "active_count": active_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
    })
