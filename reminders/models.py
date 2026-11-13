from django.db import models
from events.models import Event
from users.models import User


class Reminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reminders", verbose_name="Событие")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reminders", verbose_name="Пользователь")
    remind_before = models.PositiveIntegerField(verbose_name="За сколько дней напомнить")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    def __str__(self):
        return f"Напоминание о {self.event.title} для {self.user.name}"

    class Meta:
        ordering = ["event__event_date", "pk"]
        verbose_name = "Напоминание"
        verbose_name_plural = "Напоминания"
