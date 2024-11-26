import psycopg2


class CalendarRepository:
    def __init__(self, calendar_db_url: str, analytics_db_url: str):
        self.calendar_db_url = calendar_db_url
        self.analytics_db_url = analytics_db_url
        self._initialize_calendar_db()
        self._initialize_analytics_db()

    def _initialize_calendar_db(self):
        conn = psycopg2.connect(self.calendar_db_url)
        cursor = conn.cursor()

        # Создание таблицы календарей
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendars (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            owner TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def _initialize_analytics_db(self):
        conn = psycopg2.connect(self.analytics_db_url)
        cursor = conn.cursor()

        # Создание таблицы событий
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            action TEXT NOT NULL,
            calendar_id INTEGER,
            name TEXT,
            owner TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def create_calendar(self, name: str, owner: str) -> int:
        conn = psycopg2.connect(self.calendar_db_url)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calendars (name, owner) VALUES (%s, %s) RETURNING id",
            (name, owner)
        )
        calendar_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return calendar_id

    def update_calendar(self, calendar_id: int, name: str, owner: str):
        conn = psycopg2.connect(self.calendar_db_url)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE calendars SET name = %s, owner = %s WHERE id = %s",
            (name, owner, calendar_id)
        )
        conn.commit()
        conn.close()

    def delete_calendar(self, calendar_id: int):
        conn = psycopg2.connect(self.calendar_db_url)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calendars WHERE id = %s", (calendar_id,))
        conn.commit()
        conn.close()

    def log_event(self, action: str, calendar_id: int, name: str, owner: str):
        """Логирование событий в аналитическую базу данных."""
        conn = psycopg2.connect(self.analytics_db_url)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (action, calendar_id, name, owner) VALUES (%s, %s, %s, %s)",
            (action, calendar_id, name, owner)
        )
        conn.commit()
        conn.close()

    def get_all_calendars(self):
        conn = psycopg2.connect(self.calendar_db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calendars")
        calendars = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1], "owner": row[2]} for row in calendars]
