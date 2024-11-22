import sqlite3
import os

class CalendarRepository:
    def __init__(self):
        self.db_path = "/data/calendar.db"
        self._initialize_db()

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def create_calendar(self, name: str, owner: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO calendars (name, owner) VALUES (?, ?)", (name, owner))
        conn.commit()
        calendar_id = cursor.lastrowid
        conn.close()

        return calendar_id

    def get_all_calendars(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM calendars")
        calendars = cursor.fetchall()
        conn.close()

        return [{"id": row[0], "name": row[1], "owner": row[2]} for row in calendars]

    def delete_calendar(self, calendar_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM calendars WHERE id = ?", (calendar_id,))
        conn.commit()
        conn.close()
