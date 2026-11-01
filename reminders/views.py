import sqlite3
from datetime import date, datetime
from django.shortcuts import render
from db.database import DB_PATH


def reminders(request):
    """Страница /reminders/: список напоминаний."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT
            r.id, r.remind_before, r.is_active, r.is_sent,
            e.title AS event_title, e.event_date,
            u.name AS user_name, u.email AS user_email
        FROM reminders r
        JOIN events e ON r.event_id = e.id
        JOIN users u ON r.user_id = u.id
        ORDER BY e.event_date
    """).fetchall()
    conn.close()

    today = date.today()
    reminders_data = []
    for row in rows:
        target_date = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
        days_left = (target_date - today).days
        reminders_data.append({
            "id": row["id"],
            "event_title": row["event_title"],
            "event_date": row["event_date"],
            "user_name": row["user_name"],
            "user_email": row["user_email"],
            "remind_before": row["remind_before"],
            "days_left": days_left,
            "is_past": days_left < 0,
            "is_due": 0 <= days_left <= row["remind_before"] and row["is_active"] and not row["is_sent"],
            "is_active": bool(row["is_active"]),
            "is_sent": bool(row["is_sent"])
        })

    return render(request, "reminders/reminder_list.html", {"reminders": reminders_data})


def reminder_detail(request, reminder_id):
    """Страница /reminders/<int:reminder_id>/."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("""
        SELECT
            r.id, r.remind_before, r.is_active, r.is_sent,
            e.title AS event_title, e.event_date,
            u.name AS user_name, u.email AS user_email
        FROM reminders r
        JOIN events e ON r.event_id = e.id
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    """, [reminder_id]).fetchone()
    conn.close()

    if not row:
        return render(
            request,
            "reminders/reminder_detail.html",
            {"reminder": None},
            status=404
        )

    today = date.today()
    target_date = datetime.strptime(row["event_date"], "%Y-%m-%d").date()
    days_left = (target_date - today).days
    reminder_data = {
        "id": row["id"],
        "event_title": row["event_title"],
        "event_date": row["event_date"],
        "user_name": row["user_name"],
        "user_email": row["user_email"],
        "remind_before": row["remind_before"],
        "days_left": days_left,
        "is_past": days_left < 0,
        "is_due": 0 <= days_left <= row["remind_before"] and row["is_active"] and not row["is_sent"],
        "is_active": bool(row["is_active"]),
        "is_sent": bool(row["is_sent"])
    }

    context = {
        "reminder": reminder_data,
        "days_left": days_left,
        "is_past": days_left < 0,
        "is_due": reminder_data["is_due"],
    }
    return render(request, "reminders/reminder_detail.html", context, status=200)


def statistics(request):
    """Статистика по пользователям (SQL GROUP BY)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    stats = conn.execute("""
        SELECT
            u.name AS user_name,
            COUNT(r.id) AS reminders_count
        FROM users u
        LEFT JOIN reminders r ON u.id = r.user_id
        GROUP BY u.id, u.name
        ORDER BY reminders_count DESC
    """).fetchall()
    conn.close()

    return render(request, "reminders/statistics.html", {"statistics": stats})
