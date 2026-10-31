from django.shortcuts import render
from models.events import sort_events_by_date
from storage import load_categories, load_events, load_users


def events(request):
    """Страница /events/: список событий."""
    categories = load_categories("data/categories.json")
    users = load_users("data/users.json")
    events_list = load_events("data/events.json", categories, users)
    events_list = sort_events_by_date(events_list)
    context = {
        "events": events_list,
    }
    return render(request, "events/event_list.html", context)
