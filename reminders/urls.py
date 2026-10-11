"""Маршруты приложения reminders."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.reminders, name="reminders"),
    path(
        "<int:reminder_id>/",
        views.reminder_detail,
        name="reminder_detail",
    ),
]
