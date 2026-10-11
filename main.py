"""Точка запуска сервиса учёта важных дат (консольная версия)."""

from datetime import date

import storage
from models import Category, Event, Reminder, User
from models.events import (
    add_event,
    find_event_by_id,
    show_events,
    sort_events_by_date,
)
from models.reminders import (
    add_reminder,
    cancel_reminder,
    filter_active_reminders,
    get_due_reminders,
    show_reminders,
)
from utils import input_bool, input_date, input_int

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
EVENTS_FILE = "data/events.json"
REMINDERS_FILE = "data/reminders.json"


def create_new_reminder(
    reminders: list[Reminder],
    events: list[Event],
    users: list[User],
) -> None:
    """Создать напоминание через пользовательский сценарий."""
    event_id = input_int("id события: ")
    event = find_event_by_id(events, event_id)
    if event is None:
        print("Событие не найдено.")
        return
    user_id = input_int("id пользователя: ")
    user = storage.find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return
    remind_before = input_int("Напомнить за сколько дней: ")
    reminder = add_reminder(reminders, event, user, remind_before)
    if reminder is None:
        print("Некорректный срок напоминания.")
        return
    print(f"Напоминание добавлено, id = {reminder.id}.")


def create_new_event(
    events: list[Event],
    categories: list[Category],
    users: list[User],
) -> None:
    """Создать событие через пользовательский сценарий."""
    user_id = input_int("id пользователя: ")
    user = storage.find_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return
    category_id = input_int("id категории: ")
    category = storage.find_category_by_id(categories, category_id)
    if category is None:
        print("Категория не найдена.")
        return
    title = input("Название события: ")
    event_date = input_date("Дата (ДД.ММ.ГГГГ): ").isoformat()
    is_recurring = input_bool("Ежегодное? (да/нет): ")
    event = add_event(
        events, title, event_date, category, user, is_recurring
    )
    if event is None:
        print("Название события не может быть пустым.")
        return
    print(f"Событие добавлено, id = {event.id}.")


def show_due(reminders: list[Reminder]) -> None:
    """Вывести напоминания, которые пора показать."""
    due = get_due_reminders(reminders, date.today())
    if not due:
        print("Сегодня напоминаний нет.")
        return
    for reminder in due:
        print(reminder)


def main() -> None:
    """Основной цикл меню консольного приложения."""
    categories = storage.load_categories(CATEGORIES_FILE)
    users = storage.load_users(USERS_FILE)
    events = storage.load_events(EVENTS_FILE, categories, users)
    reminders = storage.load_reminders(REMINDERS_FILE, events, users)

    menu = (
        "\n=== Сервис учёта важных дат (консоль) ===\n"
        "1. Показать напоминания\n"
        "2. Добавить напоминание\n"
        "3. Показать сработавшие напоминания\n"
        "4. Показать только активные\n"
        "5. Отменить напоминание\n"
        "6. Показать события\n"
        "7. Добавить событие\n"
        "8. Сортировать события по дате\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_reminders(reminders)
        elif choice == 2:
            create_new_reminder(reminders, events, users)
        elif choice == 3:
            show_due(reminders)
        elif choice == 4:
            show_reminders(filter_active_reminders(reminders))
        elif choice == 5:
            reminder_id = input_int("id напоминания: ")
            if cancel_reminder(reminders, reminder_id):
                print("Напоминание отменено.")
            else:
                print("Напоминание не найдено.")
        elif choice == 6:
            show_events(events)
        elif choice == 7:
            create_new_event(events, categories, users)
        elif choice == 8:
            show_events(sort_events_by_date(events))
        elif choice == 0:
            storage.save_categories(CATEGORIES_FILE, categories)
            storage.save_users(USERS_FILE, users)
            storage.save_events(EVENTS_FILE, events)
            storage.save_reminders(REMINDERS_FILE, reminders)
            print("Данные сохранены. До встречи!")
            break
        else:
            print("Неизвестное действие.")


if __name__ == "__main__":
    main()
