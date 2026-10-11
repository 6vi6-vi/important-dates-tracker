"""Views приложения homepage: общий каркас и главная страница."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/"
    "bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с общим каркасом."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">Important Dates</a>
        <div class="navbar-nav">
            <a class="nav-link" href="/reminders/">Напоминания</a>
            <a class="nav-link" href="/events/">События</a>
        </div>
    </div>
</nav>
<div class="container">
    <h1 class="mb-4">{title}</h1>
    {content}
</div>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    content = """
    <p class="lead">
        Сервис учёта важных дат и напоминаний о них.
    </p>
    <a href="/reminders/" class="btn btn-primary">К напоминаниям</a>
    <a href="/events/" class="btn btn-secondary">К событиям</a>
    """
    return HttpResponse(page("Главная", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница 404."""
    content = """
    <p class="text-danger">Страница не найдена.</p>
    <a href="/" class="btn btn-outline-secondary">← на главную</a>
    """
    return HttpResponse(
        page("Страница не найдена", content), status=404
    )
