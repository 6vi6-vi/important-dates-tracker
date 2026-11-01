import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def events(request):
    query = request.GET.get("q", "").strip()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Запрос 3 + 8: JOIN и сортировка
    sql = """
        SELECT e.id, e.title, e.event_date, e.is_recurring,
               c.name AS category_name, u.name AS user_name
        FROM events e
        JOIN categories c ON e.category_id = c.id
        JOIN users u ON e.user_id = u.id
    """
    if query:
        sql += " WHERE e.title LIKE ?"
        events_list = conn.execute(sql + " ORDER BY e.event_date DESC", [f"%{query}%"]).fetchall()
    else:
        events_list = conn.execute(sql + " ORDER BY e.event_date DESC").fetchall()

    # Запрос 7: События без напоминаний
    lonely_events = conn.execute("""
        SELECT events.id, events.title
        FROM events
        LEFT JOIN reminders ON events.id = reminders.event_id
        WHERE reminders.id IS NULL
    """).fetchall()
    conn.close()

    return render(request, "events/event_list.html", {
        "events": events_list,
        "search_query": query,
        "lonely_events": lonely_events,
    })
