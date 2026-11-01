from django.urls import path
from . import views

app_name = "reminders"

urlpatterns = [
    path("", views.reminders, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:reminder_id>/", views.reminder_detail, name="detail"),
]
