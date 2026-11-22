from django import forms
from users.models import User
from events.models import Event


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
