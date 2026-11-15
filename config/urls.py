"""Корневая конфигурация маршрутов."""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings

handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("reminders/", include("reminders.urls")),
    path("events/", include("events.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
