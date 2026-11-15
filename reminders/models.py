from django.db import models
from events.models import Event
from users.models import User


class Reminder(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reminders", verbose_name="Событие")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reminders", verbose_name="Пользователь")
    remind_before = models.PositiveIntegerField(verbose_name="За сколько дней напомнить")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус"
    )

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    def __str__(self):
        return f"Напоминание о {self.event.title} для {self.user.name}"

    class Meta:
        ordering = ["event__event_date", "pk"]
        verbose_name = "Напоминание"
        verbose_name_plural = "Напоминания"
