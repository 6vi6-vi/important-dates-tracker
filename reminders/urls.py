from django.urls import path
from . import views

app_name = "reminders"

urlpatterns = [
    path("", views.reminders, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("create/", views.reminder_create, name="create"),
    path("<slug:slug>/", views.reminder_detail, name="detail"),
    path("<slug:slug>/edit/", views.reminder_update, name="update"),
    path("<slug:slug>/cancel/", views.reminder_cancel, name="cancel"),
]
