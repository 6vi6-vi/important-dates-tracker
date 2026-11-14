from django.shortcuts import render
from django.db.models import Q
from events.models import Event
from datetime import date


def events(request):
    query = request.GET.get("q", "").strip()
    show_past = request.GET.get("show_past", "0")
    events_qs = Event.objects.select_related("category", "user")
    if query:
        events_qs = events_qs.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
    if show_past != "1":
        events_qs = events_qs.exclude(event_date__lt=date.today())
    events_qs = events_qs.order_by("event_date")
    lonely_events = Event.objects.filter(reminders__isnull=True)

    return render(request, "events/event_list.html", {
        "events": events_qs,
        "search_query": query,
        "lonely_events": lonely_events,
        "show_past": show_past,
    })
