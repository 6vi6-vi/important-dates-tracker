import sqlite3
from django.shortcuts import render
from db.database import DB_PATH


def events(request):
    """Список событий из БД с фильтрацией и сортировкой."""
    query = request.GET.get("q", "")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    sql = """
        SELECT
            e.id, e.title, e.event_date, e.is_recurring,
            c.name AS category_name,
            u.name AS user_name
        FROM events e
        JOIN categories c ON e.category_id = c.id
        JOIN users u ON e.user_id = u.id
    """

    if query:
        sql += " WHERE e.title LIKE ?"
        sql += " ORDER BY e.event_date"
        events_list = conn.execute(sql, [f"%{query}%"]).fetchall()
    else:
        sql += " ORDER BY e.event_date"
        events_list = conn.execute(sql).fetchall()    
    conn.close()

    context = {
        "events": events_list,
        "search_query": query,
    }
    return render(request, "events/event_list.html", context)
