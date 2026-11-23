from django import forms
from users.models import User
from events.models import Event
from reminders.models import Reminder
from datetime import date
from django.core.exceptions import ValidationError


class ReminderFilterForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.order_by("title"),
        required=False,
        label="Событие",
        empty_label="Все события"
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("name"),
        required=False,
        label="Пользователь",
        empty_label="Все пользователи"
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("date", "По дате"),
            ("title", "По названию события"),
        ]
    )


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["event", "remind_before"]
        labels = {
            "event": "Событие",
            "remind_before": "За сколько дней напомнить",
        }
        help_texts = {
            "event": "Выберите событие, о котором нужно напомнить.",
            "remind_before": "Укажите количество дней до события (например, 7).",
        }
        widgets = {
            "remind_before": forms.NumberInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "remind_before": {
                "min_value": "Срок напоминания должен быть положительным.",
            }
        }

    def clean_remind_before(self):
        value = self.cleaned_data["remind_before"]
        if value < 1:
            raise forms.ValidationError("Срок напоминания должен быть положительным.")
        return value

    def clean_event(self):
        event = self.cleaned_data["event"]
        if event.event_date < date.today():
            raise ValidationError("Нельзя создать напоминание для события, которое уже прошло.")
        return event

    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get("event")
        remind_before = cleaned_data.get("remind_before")

        if event and remind_before:
            days_until_event = (event.event_date - date.today()).days

            if remind_before > days_until_event:
                raise ValidationError(
                    f"До события осталось всего {days_until_event} дн. "
                    f"Вы не можете установить напоминание за {remind_before} дн."
                )

        return cleaned_data
