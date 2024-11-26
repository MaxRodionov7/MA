import psycopg2


class CalendarRepository:
    def __init__(self, database_url: str):
        print(f"Initializing CalendarRepository with URL: {database_url}", flush=True)
        self.database_url = database_url
        self._initialize_db()

    def _initialize_db(self):
        print(f"Connecting to database with URL: {self.database_url}", flush=True)
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendars (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            owner TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def create_calendar(self, name: str, owner: str) -> int:
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO calendars (name, owner) VALUES (%s, %s) RETURNING id",
            (name, owner)
        )
        calendar_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return calendar_id

    def get_all_calendars(self):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calendars")
        calendars = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1], "owner": row[2]} for row in calendars]

    def delete_calendar(self, calendar_id: int):
        conn = psycopg2.connect(self.database_url)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calendars WHERE id = %s", (calendar_id,))
        conn.commit()
        conn.close()
