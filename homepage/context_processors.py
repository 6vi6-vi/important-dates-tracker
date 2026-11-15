from reminders.models import Reminder


def global_stats(request):
    return {
        "site_name": "Important Dates Tracker",
        "total_reminders_global": Reminder.objects.count(),
    }
