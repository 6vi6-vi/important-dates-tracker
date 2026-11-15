from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_slugs(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for event in Event.objects.all():
        base_slug = slugify(unidecode(event.title)) or "event"
        event.slug = f"{base_slug}-{event.pk}"
        event.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_event_slug'),
    ]
    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
