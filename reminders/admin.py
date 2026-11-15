from django.contrib import admin
from django import forms
from .models import Reminder
from django.utils.html import format_html


class ReminderAdminForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'status' in self.fields:
            self.fields['status'].choices = [
                (Reminder.Status.ACTIVE, "Активно"),
                (Reminder.Status.CANCELLED, "Отменено"),
            ]


class ReminderInline(admin.TabularInline):
    model = Reminder
    form = ReminderAdminForm
    fields = ("user", "remind_before", "is_sent", "status")
    extra = 0
    can_delete = False


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    form = ReminderAdminForm
    list_display = ("id", "event", "user", "remind_before", "is_sent", "display_current_status", "site_link")
    list_display_links = ("id",)
    search_fields = ("event__title", "user__name")
    list_filter = ("status", "is_sent")
    ordering = ("-id",)
    list_per_page = 20
    readonly_fields = ("id", "slug")
    view_on_site = True

    @admin.display(description="Текущий статус", ordering="status")
    def display_current_status(self, obj):
        if obj.current_status == Reminder.Status.COMPLETED:
            color = "grey"
        elif obj.current_status == Reminder.Status.CANCELLED:
            color = "red"
        else:
            color = "green"
        return format_html('<b style="color:{}">{}</b>', color, obj.status_display)

    @admin.display(description="На сайте")
    def site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Открыть</a>', obj.get_absolute_url())
