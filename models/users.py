"""Класс пользователя."""


class User:
    """Пользователь сервиса учёта важных дат."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из данных JSON."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def matches(self, query: str) -> bool:
        """Проверить совпадение имени или email с запросом."""
        query_lower = query.lower()
        return (
            query_lower in self.name.lower()
            or query_lower in self.email.lower()
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} <{self.email}>"
