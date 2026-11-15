from django.db import migrations


def migrate_statuses(apps, schema_editor):
    Reminder = apps.get_model("reminders", "Reminder")

    Reminder.objects.filter(is_active=False).update(status="cancelled")

    Reminder.objects.filter(is_active=True).update(status="active")


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0002_reminder_status'),
    ]

    operations = [
        migrations.RunPython(migrate_statuses, migrations.RunPython.noop),
    ]
