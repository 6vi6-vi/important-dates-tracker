from django.contrib import admin
from .models import Reminder


class ReminderInline(admin.TabularInline):
    model = Reminder
    fields = ("user", "remind_before", "is_sent", "is_active")
    extra = 0
    can_delete = False


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "remind_before", "is_sent", "is_active")
    list_display_links = ("id",)
    search_fields = ("event__title", "user__name")
    list_filter = ("is_active", "is_sent")
    ordering = ("-id",)
    list_per_page = 20
    list_editable = ("is_active",)
    readonly_fields = ("id",)
