"""Класс категории событий."""


class Category:
    """Категория важных дат."""

    def __init__(self, category_id: int, name: str) -> None:
        """Создать объект категории."""
        self.id = category_id
        self.name = name

    def matches(self, query: str) -> bool:
        """Проверить совпадение названия категории с запросом."""
        return query.lower() in self.name.lower()

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"
