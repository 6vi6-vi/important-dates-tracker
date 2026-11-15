from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Event
from reminders.admin import ReminderInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "event_date", "category", "user", "is_recurring", "site_link")
    list_display_links = ("title",)
    search_fields = ("title", "category__name", "user__name")
    list_filter = ("event_date", "is_recurring", "category")
    ordering = ("-event_date",)
    list_per_page = 20
    view_on_site = True
    inlines = [ReminderInline]

    @admin.display(description="На сайте")
    def site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Открыть</a>', obj.get_absolute_url())
