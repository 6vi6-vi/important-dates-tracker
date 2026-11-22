from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from events.models import Event
from datetime import date
from .forms import EventForm


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


def event_detail(request, slug):
    """Детальная страница события."""
    event = get_object_or_404(Event.objects.select_related("category", "user"), slug=slug)
    return render(request, "events/event_detail.html", {"event": event})


def event_update(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:detail", slug=event.slug)
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form, "event": event})
