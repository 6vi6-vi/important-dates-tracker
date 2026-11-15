from django.contrib import admin
from .models import Reminder
from django.utils.html import format_html


class ReminderInline(admin.TabularInline):
    model = Reminder
    fields = ("user", "remind_before", "is_sent", "status")
    extra = 0
    can_delete = False


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "remind_before", "status", "site_link")
    list_display_links = ("id",)
    search_fields = ("event__title", "user__name")
    list_filter = ("status", "is_sent")
    ordering = ("-id",)
    list_per_page = 20
    list_editable = ("status",)
    readonly_fields = ("id",)
    view_on_site = True

    @admin.display(description="На сайте")
    def site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Открыть</a>', obj.get_absolute_url())
