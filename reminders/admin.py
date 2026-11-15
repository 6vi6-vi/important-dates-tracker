from django.contrib import admin
from .models import Reminder


class ReminderInline(admin.TabularInline):
    model = Reminder
    fields = ("user", "remind_before", "is_sent", "status")
    extra = 0
    can_delete = False


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "remind_before", "is_sent", "status")
    list_display_links = ("id",)
    search_fields = ("event__title", "user__name")
    list_filter = ("status", "is_sent")
    ordering = ("-id",)
    list_per_page = 20
    list_editable = ("status",)
    readonly_fields = ("id",)
