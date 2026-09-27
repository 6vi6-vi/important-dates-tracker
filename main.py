"""Точка запуска сервиса учёта важных дат."""

from datetime import date
from typing import List

import storage
from models import Category, Event, Reminder, User
from models.events import (
    add_event,
    delete_event,
    filter_events_by_category,
    find_events,
    show_events,
    sort_events_by_date,
)
from models.reminders import (
    add_reminder,
    cancel_reminder,
    show_reminders,
    upcoming_events,
)
from utils import input_bool, input_date, input_int

CATEGORIES_FILE = "data/categories.json"
USERS_FILE = "data/users.json"
EVENTS_FILE = "data/events.json"
REMINDERS_FILE = "data/reminders.json"


def create_new_event(
    events: List[Event],
    categories: List[Category],
    users: List[User],
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


def create_new_reminder(
    reminders: List[Reminder], events: List[Event]
) -> None:
    """Создать напоминание через пользовательский сценарий."""
    event_id = input_int("id события: ")
    event = storage.find_event_by_id(events, event_id)
    if event is None:
        print("Событие не найдено.")
        return
    remind_before = input_int("Напомнить за сколько дней: ")
    reminder = add_reminder(reminders, event, remind_before)
    print(f"Напоминание добавлено, id = {reminder.id}.")


def show_upcoming(events: List[Event]) -> None:
    """Вывести предстоящие события с напоминаниями."""
    today = date.today()
    upcoming = upcoming_events(events, today)
    if not upcoming:
        print("Предстоящих событий нет.")
        return
    for event, days in upcoming:
        print(f"{event.title} — через {days} дн.")


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(user)


def show_categories(categories: List[Category]) -> None:
    """Вывести список категорий."""
    if not categories:
        print("Список категорий пуст.")
        return
    for category in categories:
        print(category)


def main() -> None:
    """Основной цикл меню приложения."""
    categories = storage.load_categories(CATEGORIES_FILE)
    users = storage.load_users(USERS_FILE)
    events = storage.load_events(EVENTS_FILE, categories, users)
    reminders = storage.load_reminders(REMINDERS_FILE, events)

    menu = (
        "\n=== Сервис учёта важных дат ===\n"
        "1. Показать события\n"
        "2. Добавить событие\n"
        "3. Найти событие по названию\n"
        "4. Фильтр по категории\n"
        "5. Показать предстоящие события\n"
        "6. Сортировать события по дате\n"
        "7. Добавить напоминание\n"
        "8. Показать напоминания\n"
        "9. Удалить событие\n"
        "10. Отменить напоминание\n"
        "11. Показать пользователей\n"
        "12. Показать категории\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_events(events)
        elif choice == 2:
            create_new_event(events, categories, users)
        elif choice == 3:
            query = input("Подстрока названия: ")
            show_events(find_events(events, query))
        elif choice == 4:
            category_id = input_int("id категории: ")
            category = storage.find_category_by_id(categories, category_id)
            if category is None:
                print("Категория не найдена.")
            else:
                show_events(filter_events_by_category(events, category))
        elif choice == 5:
            show_upcoming(events)
        elif choice == 6:
            show_events(sort_events_by_date(events))
        elif choice == 7:
            create_new_reminder(reminders, events)
        elif choice == 8:
            show_reminders(reminders)
        elif choice == 9:
            event_id = input_int("id события для удаления: ")
            if delete_event(events, event_id):
                print("Событие удалено.")
            else:
                print("Событие не найдено.")
        elif choice == 10:
            reminder_id = input_int("id напоминания: ")
            if cancel_reminder(reminders, reminder_id):
                print("Напоминание отменено.")
            else:
                print("Напоминание не найдено.")
        elif choice == 11:
            show_users(users)
        elif choice == 12:
            show_categories(categories)
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
