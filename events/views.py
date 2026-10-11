"""Views приложения events: список событий."""

from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.events import sort_events_by_date
from storage import (
    load_categories,
    load_events,
    load_users,
)


def events(request: HttpRequest) -> HttpResponse:
    """Страница /events/: список событий."""
    categories = load_categories("data/categories.json")
    users = load_users("data/users.json")
    events_list = load_events("data/events.json", categories, users)
    events_list = sort_events_by_date(events_list)

    if not events_list:
        content = '<p class="text-muted">Событий нет.</p>'
        return HttpResponse(page("События", content))

    items = ""
    for event in events_list:
        kind = "ежегодное" if event.is_recurring else "одноразовое"
        items += f"""
        <div class="list-group-item">
            <div class="d-flex justify-content-between">
                <span>{event.title}</span>
                <span class="badge bg-info text-dark">
                    {event.event_date}
                </span>
            </div>
            <small class="text-muted">
                {event.category.name}, {kind},
                пользователь: {event.user.name}
            </small>
        </div>
        """
    content = f'<div class="list-group">{items}</div>'
    return HttpResponse(page("События", content))
