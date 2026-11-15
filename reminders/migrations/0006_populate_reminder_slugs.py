from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_slugs(apps, schema_editor):
    Reminder = apps.get_model("reminders", "Reminder")
    for reminder in Reminder.objects.all():
        base_slug = slugify(unidecode(reminder.event.title)) or "reminder"
        reminder.slug = f"{base_slug}-{reminder.pk}"
        reminder.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ('reminders', '0005_reminder_slug'),
    ]
    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
