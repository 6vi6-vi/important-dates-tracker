"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json


def load_events(filename: str) -> dict[int, dict]:
    """Загрузить события из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    return {int(item["id"]): item for item in raw}


def save_events(filename: str, events: dict[int, dict]) -> None:
    """Сохранить события в JSON-файл."""
    data = list(events.values())
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_reminders(filename: str) -> list[dict]:
    """Загрузить напоминания из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_reminders(filename: str, reminders: list[dict]) -> None:
    """Сохранить напоминания в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(reminders, file, ensure_ascii=False, indent=4)
