"""Вспомогательные функции безопасного ввода."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Некорректный ввод, попробуйте снова.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Неверный формат даты, используйте ДД.ММ.ГГГГ.")


def input_bool(prompt: str) -> bool:
    """Запросить у пользователя ответ да/нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "y", "yes"):
            return True
        if answer in ("нет", "н", "n", "no"):
            return False
        print("Введите «да» или «нет».")
