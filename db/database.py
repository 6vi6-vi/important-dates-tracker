import sqlite3

DB_PATH = "data/important_dates.sqlite"


def get_connection():
    """Возвращает соединение с БД с поддержкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn
