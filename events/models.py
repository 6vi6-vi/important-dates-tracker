from datetime import datetime
from django.db import models
from users.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название события")
    event_date = models.DateField(verbose_name="Дата события")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events", verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="events", verbose_name="Пользователь")
    is_recurring = models.BooleanField(default=False, verbose_name="Ежегодное")
    title_length = models.GeneratedField(
        expression=models.Func(models.F("title"), function="LENGTH"),
        output_field=models.IntegerField(),
        db_persist=True,
        verbose_name="Длина названия"
    )
    slug = models.SlugField(max_length=180, unique=True, editable=False, verbose_name="URL-идентификатор")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title)) or "event"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["event_date", "pk"]
        verbose_name = "Событие"
        verbose_name_plural = "События"
