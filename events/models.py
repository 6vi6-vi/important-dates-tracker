from django.db import models
from users.models import User


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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["event_date", "pk"]
        verbose_name = "Событие"
        verbose_name_plural = "События"
