from datetime import date


# Создать событие
def create_event(title, event_date):
    return (
        f"Событие создано: «{title}»\n"
        f"Дата: {event_date}\n"
    )


# Расчёт количества дней до события
def days_until(event_date, today):
    gap = abs(event_date - today)
    return gap.days


# Напоминание
def get_reminder(title, days_left):
    if days_left < 0:
        return f"Событие «{title}» прошло ({abs(days_left)} дн. назад)."
    if days_left == 0:
        return f"Сегодня — «{title}»!"
    return f"До события «{title}» осталось {days_left} дн."


today = date.today()
print(f"Сегодня: {today}\n")

title = "День рождения друга"
event_date = date(2026, 10, 5)
print(create_event(title, event_date))

days_left = days_until(event_date, today)
print(f"До события осталось: {days_left} дн.")

print(get_reminder(title, days_left))
