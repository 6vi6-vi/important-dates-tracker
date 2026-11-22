from django import forms
from users.models import User
from events.models import Event
from reminders.models import Reminder


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

    def clean_remind_before(self):
        value = self.cleaned_data["remind_before"]
        if value < 1:
            raise forms.ValidationError("Срок напоминания должен быть больше 0 дней.")
        return value
