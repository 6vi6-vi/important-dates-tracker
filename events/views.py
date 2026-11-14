from django.shortcuts import render
from events.models import Event


def events(request):
    query = request.GET.get("q", "").strip()
    events_qs = Event.objects.select_related("category", "user") 
    if query:
        events_qs = events_qs.filter(title__icontains=query)     
    events_qs = events_qs.order_by("event_date")
    lonely_events = Event.objects.filter(reminders__isnull=True)

    return render(request, "events/event_list.html", {
        "events": events_qs,
        "search_query": query,
        "lonely_events": lonely_events,
    })
