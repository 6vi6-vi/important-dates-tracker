"""Точка запуска сервиса учёта важных дат."""

from datetime import date

import storage
from models.events import (
    add_event,
    delete_event,
    filter_events_by_category,
    find_events,
)
from models.reminders import (
    add_reminder,
    cancel_reminder,
    upcoming_events,
)
from utils import input_bool, input_date, input_int

EVENTS_FILE = "data/events.json"
REMINDERS_FILE = "data/reminders.json"


def show_events(events: dict[int, dict]) -> None:
    """Вывести список событий."""
    if not events:
        print("Список событий пуст.")
        return
    for event_id, data in events.items():
        recurring = "ежегодное" if data["is_recurring"] else "одноразовое"
        print(
            f"[{event_id}] {data['title']} — {data['event_date']} "
            f"({data['category']}, {recurring})"
        )


def show_reminders(reminders: list[dict]) -> None:
    """Вывести список напоминаний."""
    if not reminders:
        print("Список напоминаний пуст.")
        return
    for reminder in reminders:
        print(
            f"[{reminder['id']}] событие {reminder['event_id']}, "
            f"за {reminder['remind_before']} дн."
        )


def show_upcoming(events: dict[int, dict]) -> None:
    """Вывести предстоящие события с напоминаниями."""
    today = date.today()
    upcoming = upcoming_events(events, today)
    if not upcoming:
        print("Предстоящих событий нет.")
        return
    for data, days in upcoming:
        print(f"{data['title']} — через {days} дн.")


def main() -> None:
    """Основной цикл меню приложения."""
    events = storage.load_events(EVENTS_FILE)
    reminders = storage.load_reminders(REMINDERS_FILE)

    menu = (
        "\n=== Сервис учёта важных дат ===\n"
        "1. Показать события\n"
        "2. Добавить событие\n"
        "3. Найти событие по названию\n"
        "4. Фильтр по категории\n"
        "5. Показать предстоящие события\n"
        "6. Добавить напоминание\n"
        "7. Показать напоминания\n"
        "8. Удалить событие\n"
        "9. Отменить напоминание\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_events(events)
        elif choice == 2:
            title = input("Название события: ")
            event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            category = input("Категория: ")
            is_recurring = input_bool("Ежегодное? (да/нет): ")
            new_id = add_event(
                events, title, event_date, category, is_recurring
            )
            print(f"Событие добавлено, id = {new_id}.")
        elif choice == 3:
            query = input("Подстрока названия: ")
            found = find_events(events, query)
            show_events(found)
        elif choice == 4:
            category = input("Категория: ")
            found = filter_events_by_category(events, category)
            show_events(found)
        elif choice == 5:
            show_upcoming(events)
        elif choice == 6:
            event_id = input_int("id события: ")
            remind_before = input_int("Напомнить за сколько дней: ")
            add_reminder(reminders, event_id, remind_before)
            print("Напоминание добавлено.")
        elif choice == 7:
            show_reminders(reminders)
        elif choice == 8:
            event_id = input_int("id события для удаления: ")
            if delete_event(events, event_id):
                print("Событие удалено.")
            else:
                print("Событие не найдено.")
        elif choice == 9:
            reminder_id = input_int("id напоминания: ")
            if cancel_reminder(reminders, reminder_id):
                print("Напоминание отменено.")
            else:
                print("Напоминание не найдено.")
        elif choice == 0:
            storage.save_events(EVENTS_FILE, events)
            storage.save_reminders(REMINDERS_FILE, reminders)
            print("Данные сохранены. До встречи!")
            break
        else:
            print("Неизвестное действие.")


if __name__ == "__main__":
    main()
