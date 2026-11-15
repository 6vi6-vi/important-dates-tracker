from django.db import models
from events.models import Event
from users.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse


class Reminder(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reminders", verbose_name="Событие")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="reminders", verbose_name="Пользователь")
    remind_before = models.PositiveIntegerField(verbose_name="За сколько дней напомнить")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")
    slug = models.SlugField(max_length=200, unique=True, editable=False, verbose_name="URL-идентификатор")

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус"
    )

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.event.title)) or "reminder"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("reminders:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"Напоминание о {self.event.title} для {self.user.name}"

    class Meta:
        ordering = ["event__event_date", "pk"]
        verbose_name = "Напоминание"
        verbose_name_plural = "Напоминания"
