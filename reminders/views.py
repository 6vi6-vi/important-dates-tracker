import sqlite3
from datetime import date, datetime
from django.shortcuts import render
from db.database import DB_PATH


def reminders(request):
    filter_type = request.GET.get("filter", "all")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    sql = """
        SELECT r.id, r.remind_before, r.is_active, r.is_sent,
               e.title AS event_title, e.event_date, u.name AS user_name
        FROM reminders r
        JOIN events e ON r.event_id = e.id
        JOIN users u ON r.user_id = u.id
    """

    today_str = date.today().isoformat()
    if filter_type == "active":
        # Только активные и ещё не прошедшие события
        sql += " WHERE r.is_active = 1 AND e.event_date >= ?"
        rows = conn.execute(sql + " ORDER BY e.event_date", [today_str]).fetchall()
    elif filter_type == "past":
        # Только прошедшие события
        sql += " WHERE e.event_date < ?"
        rows = conn.execute(sql + " ORDER BY e.event_date DESC", [today_str]).fetchall()
    elif filter_type == "inactive":
        # Только отменённые
        sql += " WHERE r.is_active = 0"
        rows = conn.execute(sql + " ORDER BY e.event_date").fetchall()
    else:
        # Все напоминания (Запрос 1)
        rows = conn.execute(sql + " ORDER BY e.event_date").fetchall()
    conn.close()

    today = date.today()
    reminders_data = []
    for row in rows:
        target_date = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
        days_left = (target_date - today).days
        reminders_data.append({
            "id": row["id"], "event_title": row["event_title"], "event_date": row["event_date"],
            "user_name": row["user_name"], "remind_before": row["remind_before"],
            "days_left": days_left, "is_past": days_left < 0,
            "is_due": 0 <= days_left <= row["remind_before"] and row["is_active"] and not row["is_sent"],
            "is_active": bool(row["is_active"]), "is_sent": bool(row["is_sent"])
        })

    return render(request, "reminders/reminder_list.html", {
        "reminders": reminders_data,
        "filter_type": filter_type
    })


def reminder_detail(request, reminder_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Запрос 10 (WHERE по ID) + Запрос 4 (JOIN)
    query = """
        SELECT r.id, r.remind_before, r.is_active, r.is_sent,
               e.title AS event_title, e.event_date, u.name AS user_name, u.email AS user_email
        FROM reminders r
        JOIN events e ON r.event_id = e.id
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    """
    row = conn.execute(query, [reminder_id]).fetchone()
    conn.close()

    if not row:
        return render(request, "reminders/reminder_detail.html", {"reminder": None}, status=404)

    today = date.today()
    target_date = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
    days_left = (target_date - today).days
    reminder_data = {
        "id": row["id"], "event_title": row["event_title"], "event_date": row["event_date"],
        "user_name": row["user_name"], "user_email": row["user_email"], "remind_before": row["remind_before"],
        "is_active": bool(row["is_active"]), "is_sent": bool(row["is_sent"])
    }

    return render(request, "reminders/reminder_detail.html", {
        "reminder": reminder_data, "days_left": days_left,
        "is_past": days_left < 0, "is_due": 0 <= days_left <= row["remind_before"] and row["is_active"] and not row["is_sent"]
    }, status=200)


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Запрос 6: Статистика по пользователям (GROUP BY)
    stats = conn.execute("""
        SELECT u.name AS user_name, COUNT(r.id) AS reminders_count
        FROM users u
        LEFT JOIN reminders r ON u.id = r.user_id
        GROUP BY u.id, u.name
        ORDER BY reminders_count DESC
    """).fetchall()

    # Запрос 5: Общее количество активных напоминаний (COUNT + WHERE)
    active_count = conn.execute("SELECT COUNT(*) AS active_reminders FROM reminders WHERE is_active = 1").fetchone()["active_reminders"]
    conn.close()

    return render(request, "reminders/statistics.html", {
        "statistics": stats,
        "active_count": active_count
    })
